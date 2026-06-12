import { render, screen } from '@testing-library/react';
import DashboardPage from '../src/app/dashboard/page';

describe('DashboardPage', () => {
  it('renders the dashboard heading', () => {
    render(<DashboardPage />);
    const heading = screen.getByRole('heading', { level: 1, name: /Dashboard/i });
    expect(heading).toBeDefined();
  });
});
