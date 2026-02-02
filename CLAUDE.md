# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Sony Interior** - a Next.js 15-based interior design and furniture showcase website with an integrated AI chatbot assistant. The application features modern UI animations, smooth scrolling effects, and an AI-powered furniture consultation chatbot using Google's Gemini 2.5 Flash model.

## Commands

### Development
```bash
pnpm dev              # Start development server with Turbopack
pnpm build            # Build for production
pnpm start            # Start production server
pnpm lint             # Run ESLint
```

This project uses **pnpm** as the package manager (v10.10.0).

## Architecture

### Tech Stack
- **Framework**: Next.js 15.3.8 (App Router)
- **React**: v19 with Server Components
- **TypeScript**: Type-safe development
- **Styling**: Tailwind CSS with shadcn/ui components
- **Animation**: Framer Motion, GSAP, Lenis smooth scroll
- **AI Integration**: Vercel AI SDK with Google Gemini 2.5 Flash
- **UI Components**: Radix UI primitives via shadcn/ui

### Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── api/chat/          # AI chatbot API route
│   ├── layout.tsx         # Root layout with Navbar, Footer, ChatWidget
│   ├── page.tsx           # Homepage composition
│   └── globals.css        # Global styles and Tailwind layers
├── components/            # React components
│   ├── ui/               # shadcn/ui components (auto-generated)
│   ├── Hero.tsx          # Landing hero section
│   ├── ZoomParallax.tsx  # Animated parallax gallery
│   ├── ChatWidget.tsx    # AI chatbot UI
│   ├── Navbar.tsx        # Navigation
│   └── Footer.tsx        # Footer
├── lib/
│   ├── utils.ts          # cn() utility for class merging
│   └── data.ts           # AI system prompt configuration
├── hooks/                # Custom React hooks
└── assets/               # Static images
```

### Key Architecture Patterns

**1. App Router Layout**
- `layout.tsx` provides global layout with Navbar, Footer, and ChatWidget rendered on all pages
- Pages compose multiple section components (Hero, ZoomParallax, BestInterior, etc.)

**2. AI Chatbot System**
- **API Route**: `/api/chat/route.ts` handles streaming responses using Vercel AI SDK
- **Model**: Google Gemini 2.5 Flash (`gemini-2.5-flash`)
- **System Prompt**: Defined in `src/lib/data.ts` as `initialMessage`
- **Guardrails**: Bot only responds to Sony Interior/furniture-related queries
- **UI**: Floating chat widget (`ChatWidget.tsx`) with animated open/close states

**3. Animation Libraries**
- **Framer Motion**: Component animations, parallax effects, scroll-based transforms
- **Lenis**: Smooth scroll behavior (used in `ZoomParallax.tsx`)
- **GSAP**: Advanced animation sequences (installed but usage varies)

**4. Component System**
- shadcn/ui components in `src/components/ui/` (do not manually edit - regenerate via CLI)
- Custom components compose UI primitives from `ui/`
- Use `cn()` utility from `@/lib/utils` for conditional className merging

**5. Styling Approach**
- Tailwind CSS with custom color scheme: `primaryDark`, `lightOrange`, `darkGray`, `lightGray`
- CSS custom properties for theme tokens in `globals.css`
- Custom utility classes in `@layer utilities` for complex layouts (`.img-shadow`, `.item`, etc.)

### Path Aliases
- `@/*` → `./src/*`
- Configured in both `tsconfig.json` and `components.json`

### Image Configuration
- External images allowed from `images.unsplash.com` (see `next.config.ts`)
- Local images stored in `src/assets/` and `src/assets/images/`

### AI Chatbot Behavior
- The AI assistant is scoped to Sony Interior furniture/décor queries only
- System prompt includes markdown formatting instructions (bold, italics, bullet points)
- Responses stream in real-time using `useChat()` hook from `@ai-sdk/react`
- Token usage logged on each request (see `route.ts`)

### shadcn/ui Integration
- Configuration: `components.json`
- Style: `new-york` variant
- Components auto-installed to `src/components/ui/`
- Use `npx shadcn@latest add <component>` to add new components

## Development Notes

### Adding UI Components
Use the shadcn/ui CLI to add components:
```bash
npx shadcn@latest add button
npx shadcn@latest add dialog
```

### Working with Animations
- ZoomParallax uses scroll-linked transforms - modify `scale` values in `useTransform()` calls
- Lenis smooth scroll is initialized in `useEffect()` - ensure cleanup if modifying scroll behavior
- Framer Motion variants are defined inline - extract to constants for reusability

### Modifying AI Behavior
- Edit system prompt in `src/lib/data.ts` (`initialMessage`)
- Change model in `src/app/api/chat/route.ts` (currently `gemini-2.5-flash`)
- Ensure API keys are set in environment variables (Google AI SDK expects `GOOGLE_GENERATIVE_AI_API_KEY`)

### Custom Colors
Reference Tailwind config colors:
- `primaryDark` / `darkGray`: #1a1f25
- `lightGray`: #272c35
- `lightOrange`: #F5F9E9

### TypeScript Configuration
- Target: ES2017
- Strict mode enabled
- JSX: preserve (handled by Next.js)
