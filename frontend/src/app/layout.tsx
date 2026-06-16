import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ASTRA",
  description: "ASTRA Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <header className="bg-gray-900 text-white p-4">
            <h1 className="text-xl font-bold">ASTRA</h1>
          </header>
          <div className="flex flex-1">
            <nav className="w-64 bg-gray-100 p-4">
              <ul>
                <li className="mb-2"><Link href="/" className="hover:underline">Home</Link></li>
                <li className="mb-2"><Link href="/dashboard" className="hover:underline">Dashboard</Link></li>
              </ul>
            </nav>
            <main className="flex-1 bg-white">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
