import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title:"The Doll Atelier — Bespoke Antique Doll Dressmaking", description:"One-of-one, hand-sewn heirloom garments for antique dolls, commissioned worldwide.", icons:{icon:"/favicon.svg",shortcut:"/favicon.svg"} };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body>{children}</body></html>; }
