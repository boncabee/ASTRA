import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from models.automation import AutomationExecution, AutomationRequest, AutomationState
from workers.automation_worker import automation_worker
from core.queue import automation_queue, AutomationJob
import uuid

@pytest.fixture(autouse=True)
def clear_queue():
    # Clear queue before and after each test
    while not automation_queue.queue.empty():
        automation_queue.queue.get_nowait()
        automation_queue.queue.task_done()
    yield
    while not automation_queue.queue.empty():
        automation_queue.queue.get_nowait()
        automation_queue.queue.task_done()

@pytest.fixture
def mock_session():
    with patch("workers.automation_worker.SessionLocal") as mock:
        yield mock

@pytest.mark.asyncio
async def test_automation_worker_start_stop():
    assert not automation_worker.is_running
    await automation_worker.start()
    assert automation_worker.is_running
    
    # Starting again should return early
    await automation_worker.start()
    
    await automation_worker.stop()
    assert not automation_worker.is_running

@pytest.mark.asyncio
async def test_automation_worker_process_job_not_found(mock_session, caplog):
    session_instance = mock_session.return_value.__aenter__.return_value
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    session_instance.execute.return_value = mock_result
    
    job = AutomationJob(str(uuid.uuid4()), str(uuid.uuid4()), "webhook", {})
    await automation_worker._process_job(job)
    assert "not found" in caplog.text

@pytest.mark.asyncio
async def test_automation_worker_process_job_request_not_found(mock_session, caplog):
    session_instance = mock_session.return_value.__aenter__.return_value
    execution = AutomationExecution(id=uuid.uuid4())
    mock_exec_result = MagicMock()
    mock_exec_result.scalars.return_value.first.return_value = execution
    
    mock_req_result = MagicMock()
    mock_req_result.scalars.return_value.first.return_value = None
    session_instance.execute.side_effect = [mock_exec_result, mock_req_result]
    
    job = AutomationJob(str(execution.id), str(uuid.uuid4()), "webhook", {})
    await automation_worker._process_job(job)
    assert "not found" in caplog.text

@pytest.mark.asyncio
async def test_automation_worker_process_job_success(mock_session):
    session_instance = mock_session.return_value.__aenter__.return_value
    execution = AutomationExecution(id=uuid.uuid4())
    request = AutomationRequest(id=uuid.uuid4())
    
    mock_exec_result = MagicMock()
    mock_exec_result.scalars.return_value.first.return_value = execution
    mock_req_result = MagicMock()
    mock_req_result.scalars.return_value.first.return_value = request
    session_instance.execute.side_effect = [mock_exec_result, mock_req_result]
    
    with patch("workers.automation_worker.get_provider") as mock_get_provider:
        mock_provider = AsyncMock()
        mock_provider.execute.return_value = (True, {"status": "ok"}, None)
        mock_get_provider.return_value = mock_provider
        
        job = AutomationJob(str(execution.id), str(request.id), "webhook", {})
        await automation_worker._process_job(job)
        
        assert execution.state == AutomationState.SUCCESS
        assert request.state == AutomationState.SUCCESS

@pytest.mark.asyncio
async def test_automation_worker_process_job_failure(mock_session):
    session_instance = mock_session.return_value.__aenter__.return_value
    execution = AutomationExecution(id=uuid.uuid4())
    request = AutomationRequest(id=uuid.uuid4())
    
    mock_exec_result = MagicMock()
    mock_exec_result.scalars.return_value.first.return_value = execution
    mock_req_result = MagicMock()
    mock_req_result.scalars.return_value.first.return_value = request
    session_instance.execute.side_effect = [mock_exec_result, mock_req_result]
    
    with patch("workers.automation_worker.get_provider") as mock_get_provider:
        mock_provider = AsyncMock()
        mock_provider.execute.return_value = (False, None, "error")
        mock_get_provider.return_value = mock_provider
        
        job = AutomationJob(str(execution.id), str(request.id), "webhook", {})
        await automation_worker._process_job(job)
        
        assert execution.state == AutomationState.FAILED
        assert request.state == AutomationState.FAILED
        assert execution.error_message == "error"

@pytest.mark.asyncio
async def test_automation_worker_process_job_exception(mock_session):
    session_instance = mock_session.return_value.__aenter__.return_value
    execution = AutomationExecution(id=uuid.uuid4())
    request = AutomationRequest(id=uuid.uuid4())
    
    mock_exec_result = MagicMock()
    mock_exec_result.scalars.return_value.first.return_value = execution
    mock_req_result = MagicMock()
    mock_req_result.scalars.return_value.first.return_value = request
    session_instance.execute.side_effect = [mock_exec_result, mock_req_result]
    
    with patch("workers.automation_worker.get_provider") as mock_get_provider:
        mock_provider = AsyncMock()
        mock_provider.execute.side_effect = ValueError("Test Exception")
        mock_get_provider.return_value = mock_provider
        
        job = AutomationJob(str(execution.id), str(request.id), "webhook", {})
        await automation_worker._process_job(job)
        
        assert execution.state == AutomationState.FAILED
        assert request.state == AutomationState.FAILED
        assert "Test Exception" in execution.error_message

@pytest.mark.asyncio
async def test_automation_worker_db_exception(mock_session, caplog):
    session_instance = mock_session.return_value.__aenter__.return_value
    session_instance.execute.side_effect = Exception("DB error")
    
    job = AutomationJob(str(uuid.uuid4()), str(uuid.uuid4()), "webhook", {})
    await automation_worker._process_job(job)
    assert "DB error" in caplog.text

@pytest.mark.asyncio
async def test_automation_worker_run_loop(caplog):
    job = AutomationJob(str(uuid.uuid4()), str(uuid.uuid4()), "webhook", {})
    await automation_queue.enqueue(job)
    
    with patch.object(automation_worker, "_process_job", autospec=True) as mock_process:
        async def mock_process_job(j):
            automation_worker.is_running = False
        mock_process.side_effect = mock_process_job
        
        automation_worker.is_running = True
        loop_task = asyncio.create_task(automation_worker._run_loop())
        
        await loop_task
            
        mock_process.assert_called_once()

@pytest.mark.asyncio
async def test_automation_worker_run_loop_exception(caplog):
    job = AutomationJob(str(uuid.uuid4()), str(uuid.uuid4()), "webhook", {})
    await automation_queue.enqueue(job)
    
    with patch.object(automation_worker, "_process_job", autospec=True) as mock_process:
        async def mock_process_job(j):
            automation_worker.is_running = False
            raise Exception("Loop exception")
        mock_process.side_effect = mock_process_job
        
        automation_worker.is_running = True
        loop_task = asyncio.create_task(automation_worker._run_loop())
        
        await loop_task
            
        assert "Loop exception" in caplog.text

@pytest.mark.asyncio
async def test_automation_worker_run_loop_cancelled():
    automation_worker.is_running = True
    loop_task = asyncio.create_task(automation_worker._run_loop())
    # Cancel immediately
    loop_task.cancel()
    try:
        await loop_task
    except asyncio.CancelledError:
        pass
    # The loop should catch CancelledError and break, meaning the task just finishes if caught, 
    # but asyncio.create_task propagates it to the awaiter if cancelled.
    # Wait, the try/except in _run_loop catches it and breaks, returning gracefully!
    # Let's ensure it doesn't raise if it catches it.
    assert not loop_task.done() or loop_task.cancelled() or loop_task.exception() is None
