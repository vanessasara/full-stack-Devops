import type { Metadata } from "next";
import { Playfair_Display, Inter } from 'next/font/google';
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ChatWidget from "@/components/ChatWidget";

const playfair = Playfair_Display({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-playfair',
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: "Sony Interior - Modern Furniture & Home Décor",
  description: "Discover sophisticated furniture designs and elegant home décor at Sony Interior. Transform your space with our curated collection of modern interior pieces.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${playfair.variable} ${inter.variable}`}>
      <body className={inter.className}>
        <Navbar />
        {children}
        <ChatWidget/>
        <Footer/>
      </body>
    </html>
  );
}
