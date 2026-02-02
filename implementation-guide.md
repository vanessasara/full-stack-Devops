# CLAUDE_CODE_GUIDE.md

## Project Overview

You are transforming **Sony Interior** from a basic furniture website into a sophisticated e-commerce platform with an AI-powered RAG chatbot. This is a complete rebuild focusing on exceptional UI/UX, Sanity CMS integration, MCP servers for real-time data access, and an intelligent chatbot using OpenAI Agent SDK routed through LiteLLM to Gemini (NO OpenAI keys required).

---

## CRITICAL: Technology Stack Understanding

**AI Agent Setup (MOST IMPORTANT):**
- Use OpenAI Agent SDK but route EVERYTHING through LiteLLM to Gemini
- User has ONLY Gemini API key, NEVER use or reference OpenAI keys
- Follow the exact pattern from user's example code structure
- Import Agent, Runner, function_tool, set_tracing_disabled from agents package
- Import LitellmModel from agents.extensions.models.litellm_model
- Always use async/await with Runner.run() method
- Set tracing disabled to reduce logging overhead
- Model string format: `gemini/gemini-2.0-flash` or `gemini/gemini-2.5-flash`
- All agent tools use the function_tool decorator

**MCP Integration Architecture:**
- MCP (Model Context Protocol) servers provide real-time data access to the agent
- Create separate MCP servers for Sanity CMS and Neon Database
- Agent tools call MCP servers instead of making direct API calls
- This gives the chatbot fresh, accurate data without embedding lag
- MCP servers run as separate processes alongside FastAPI backend

**Animation Libraries:**
- Keep GSAP installed - use for hero section, scroll-triggered effects, complex timeline animations
- Keep Framer Motion - use for component transitions and simple animations
- Use both strategically where each excels

---

## Environment Variables

Create `.env.local` file at project root with these variables. Leave ALL values empty - user will fill them manually:

```
# AI Model (ONLY GEMINI - NO OPENAI KEY NEEDED)
GEMINI_API_KEY=

# Sanity CMS
NEXT_PUBLIC_SANITY_PROJECT_ID=
NEXT_PUBLIC_SANITY_DATASET=
SANITY_API_TOKEN=

# Neon Serverless Postgres
DATABASE_URL=

# Backend URLs
PYTHON_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:3000

# MCP Server URLs (local development)
MCP_SANITY_SERVER_URL=http://localhost:3001
MCP_DATABASE_SERVER_URL=http://localhost:3002
```

**Where to Get These Keys:**

**Gemini API Key:**
- Visit Google AI Studio at aistudio.google.com/apikey
- Sign in with Google account
- Click "Create API Key" button
- Copy the generated key (starts with AIza)
- This is the ONLY AI key needed for the entire project

**Sanity Credentials:**
- Project ID: Found in Sanity dashboard URL or sanity.config.ts file
- Dataset: Usually named "production"
- API Token: In Sanity dashboard go to API section, click Tokens tab, create new token with Read permissions, copy the token value

**Neon Database URL:**
- Go to neon.tech and sign up or log in
- Click "New Project" button
- Name your project (example: sony-interior-database)
- Select region closest to where you'll deploy (US East for Vercel)
- Wait for project creation (takes 30 seconds)
- Go to project Dashboard
- Find "Connection Details" or "Connection String" section
- Copy the entire connection string which looks like:
  postgresql://username:password@ep-something-123456.region.aws.neon.tech/dbname?sslmode=require
- This complete string is your DATABASE_URL
- Neon provides this ready-to-use, no need to construct it yourself

---

## PHASE 1: Clean Slate and Dependency Updates

### Goals
Update all dependencies to latest versions, ensure development server runs without errors, prepare project structure for major rebuild.

### Tasks

**Package Updates:**
- Run pnpm update command to update all packages to latest stable versions
- After update completes, run pnpm install to ensure lock file is correct
- Verify package.json shows Next.js version fifteen point three or higher
- Confirm React is on version nineteen
- Check Framer Motion is latest version
- Check GSAP is latest stable version (DO NOT REMOVE IT)
- Verify Tailwind CSS and PostCSS are latest versions
- Update Vercel AI SDK packages: ai and @ai-sdk/react for frontend useChat hook
- Update all shadcn/ui components by running: npx shadcn@latest add button (and other components you're using)
- Ensure typescript and related type packages are up to date

**Development Server Test:**
- Run pnpm dev command
- Verify server starts successfully on localhost:3000
- Check that homepage loads without errors
- Test all existing pages (if any) load correctly
- Open browser console and verify no JavaScript errors
- Check that existing animations work smoothly
- Test ZoomParallax component if it exists
- Verify Lenis smooth scroll functions properly
- Fix any TypeScript compilation errors that appear
- Address any console warnings

**Project Structure Setup:**
- In src folder ensure lib directory exists
- Create lib/data folder for storing static text content
- Create lib/constants folder for reusable constant values
- Create lib/types folder for all TypeScript interfaces
- Create lib/utils folder if missing
- Create lib/sanity folder for Sanity-related utilities
- Verify components folder has proper organization
- Ensure globals.css file exists in app directory

**Code Cleanup:**
- Go through all existing component files
- Remove any unused imports
- Remove any console.log statements
- Check all useEffect hooks have proper cleanup return functions
- Verify animation cleanup especially for GSAP and Lenis
- Remove any dead code or commented-out sections
- Ensure all images have descriptive alt text attributes
- Check responsive design works on mobile, tablet, and desktop viewports

**Next.js Configuration:**
- Open next.config.ts file
- In images configuration add Unsplash domains
- Add remotePatterns for images.unsplash.com
- Add remotePatterns for cdn.sanity.io for Sanity images
- Ensure experimental features are properly configured if needed
- Verify TypeScript strict mode is enabled

---

## PHASE 2: Complete UI/UX Redesign - Planning and Foundation

### Goals
Design and implement a stunning, modern furniture website interface that makes products the hero. Create visual hierarchy, generous whitespace, and smooth interactions that feel premium.

### Understanding Modern Furniture Website Design

**Design Philosophy:**
- Large high-quality product photography as primary focus
- Generous whitespace between elements to let products breathe
- Minimal text with strong typography hierarchy
- Neutral sophisticated color palette with strategic accent colors
- Smooth subtle animations that enhance user experience
- Grid-based layouts for product displays
- Clean intuitive navigation
- Mobile-first responsive approach

**Reference Aesthetic:**
- Study brands like West Elm, Article, Burrow, Interior Define, Floyd
- Modern minimalist with warm approachable touches
- Professional photography with lifestyle context
- Clear calls-to-action without being pushy

### Tasks

**Color System Definition:**
- Open globals.css or create tailwind.config.ts modifications
- Define primary colors: Deep charcoal or navy for text and headers
- Define secondary colors: Warm cream or soft beige for backgrounds
- Define accent color: Terracotta, sage green, or warm gold for CTAs and highlights
- Define neutral grays palette for borders, subtle backgrounds, disabled states
- Ensure all color combinations meet WCAG accessibility contrast ratios
- Create CSS custom properties or Tailwind theme extensions for consistency
- Test colors in both light mode (primary focus)

**Typography System:**
- Choose serif font for headings: Playfair Display, Crimson Text, or Lora
- Choose sans-serif for body: Inter, Work Sans, or DM Sans
- Add font imports to layout.tsx or globals.css using next/font
- Define heading sizes: h1 (48-64px), h2 (36-48px), h3 (28-36px), h4 (20-24px), h5 (18-20px), h6 (16-18px)
- Set body text size to 16px with line-height 1.6 for readability
- Define font weights: regular 400, medium 500, semibold 600, bold 700
- Create reusable typography classes in globals.css
- Ensure responsive font sizes scale down appropriately on mobile

**Spacing System:**
- Establish consistent spacing scale using Tailwind defaults or custom values
- Use spacing multiples: 4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px
- Apply generous margins between major sections (64px-128px on desktop)
- Use consistent padding within components
- Ensure mobile spacing is proportionally reduced but still comfortable

**Component Library Foundation:**
- In globals.css create base component styles that will be reused
- Define button styles: primary, secondary, outline variants
- Create card component base styles
- Define input field styles
- Create hover and focus state styles
- Ensure all interactive elements have clear visual feedback
- Store these as CSS classes to avoid repetition across components

---

## PHASE 3: Homepage Redesign - Implementation

### Goals
Build a stunning homepage that immediately communicates brand quality and showcases products effectively. Each section should have purpose and flow naturally.

### Tasks

**Hero Section (Full Viewport):**
- Use existing hero images from assets folder or fetch high-quality furniture lifestyle image from Unsplash
- Make hero full viewport height using h-screen class
- Add gradient overlay on image for text readability (dark gradient from top or bottom)
- Position content in center or left-aligned
- Main headline: Large bold text like "Transform Your Space" or "Timeless Furniture for Modern Living"
- Subheadline: One sentence value proposition explaining what makes Sony Interior special
- Primary CTA button: "Explore Collection" or "Shop Now" linking to products page
- Use GSAP for hero animations: headline fades in and slides up, subheadline follows with delay, CTA button appears last
- Add subtle parallax effect to background image using GSAP ScrollTrigger or Framer Motion
- Ensure responsive: stack elements vertically centered on mobile, reduce text sizes

**Featured Products Section:**
- Section headline: "Featured Collection" or "Best Sellers" centered with margin-bottom
- Fetch three to six featured products from Sanity using featured boolean field
- Create grid layout: three columns on desktop (lg:grid-cols-3), two on tablet (md:grid-cols-2), one on mobile
- Each product card structure: image container with aspect-ratio-square or 3:4, product name, price, quick view or shop button
- Card hover effects: image zooms slightly using scale transform, card lifts with shadow, button changes color
- Use Framer Motion for stagger animation when cards enter viewport
- Each card links to individual product detail page using href to /products/[slug]
- Add loading skeleton states while products fetch
- Handle empty state gracefully if no featured products exist

**About Preview Section:**
- Two-column layout on desktop: text content left (50%), image right (50%)
- Section headline: "Our Story" or "About Sony Interior"
- Paragraph of text (two to three sentences) about company philosophy, craftsmanship, or design approach
- User will write this copy later so leave placeholder Lorem ipsum
- CTA link: "Learn More" linking to /about page
- Use Framer Motion: text slides in from left, image slides in from right on scroll into view
- On mobile: stack vertically with image on top, text below
- Choose complementary image from Unsplash showing craftsmanship or showroom

**Categories Showcase Section:**
- Section headline: "Shop by Category" centered
- Display main furniture categories: Sofas, Chairs, Tables, Beds, Lighting, Storage
- Large clickable category cards in grid: three columns desktop, two tablet, one mobile
- Each card: background image of category, semi-transparent overlay, category name centered
- Hover effect: overlay lightens or darkens, name becomes more prominent, subtle zoom on image
- Link each card to products page with category filter: /products?category=sofas
- Use GSAP ScrollTrigger for cards revealing with stagger effect as user scrolls
- Fetch category images from Unsplash with relevant search terms

**Social Proof or Values Section:**
- Optional section showing trust signals
- Grid of icons with text: Free Shipping, Quality Guarantee, Easy Returns, Sustainable Materials
- Each item: icon, headline, short description
- Center aligned with even spacing
- Subtle entrance animation using Framer Motion
- Keep minimal and clean without overwhelming

**Newsletter Signup Section:**
- Background color different from main page for visual separation
- Centered layout with headline: "Stay Inspired"
- Subtext: "Get design tips and exclusive offers"
- Email input field with submit button
- Form submission will be handled later, for now just UI
- Ensure accessible form labels and validation states
- Responsive: full width on mobile with stacked button

---

## PHASE 4: Navigation and Footer Implementation

### Goals
Create intuitive, responsive navigation that works seamlessly across devices and a comprehensive footer with all necessary links.

### Tasks

**Desktop Navigation Bar:**
- Create Navbar component in components folder
- Fixed position at top with backdrop blur effect
- Logo on left side, menu items in center, icons (search, cart) on right
- Menu items: Home, About, Products, Contact
- Initially transparent over hero, becomes solid white/cream background on scroll
- Use Framer Motion or state to handle scroll-based background change
- Active page indicator: underline or different color for current page
- Hover effects on menu items: subtle underline animation
- Ensure proper z-index so it stays above other content
- Smooth transitions for all state changes

**Mobile Navigation:**
- Hamburger menu icon (three horizontal lines) in top right on mobile screens
- Hide desktop menu items below md breakpoint, show hamburger
- On click: full-screen drawer slides in from right side
- Drawer contains: logo at top, menu items stacked vertically, close button (X icon)
- Use Framer Motion AnimatePresence for smooth drawer animation
- Overlay background with dark semi-transparent backdrop
- Clicking outside drawer or close button dismisses it
- Prevent body scroll when drawer is open
- Menu items in drawer should be large and touch-friendly

**Footer Component:**
- Multi-column layout on desktop: four columns
- Column one: About Sony Interior with short description, logo
- Column two: Quick Links (Home, About, Products, Contact)
- Column three: Customer Service (Shipping Info, Returns, FAQ, Terms)
- Column four: Newsletter signup and social media icons
- Include store address and contact information
- Copyright notice at bottom center
- On mobile: stack columns vertically with proper spacing
- Use semantic HTML footer tag
- Ensure all links are functional or marked as placeholder
- Social media icons: Instagram, Facebook, Pinterest placeholders
- Keep styling consistent with overall design system

---

## PHASE 5: About Page Design and Implementation

### Goals
Create a compelling About page that tells Sony Interior's story and builds trust with customers.

### Tasks

**Page Structure Planning:**
- Create app/about/page.tsx file
- Add metadata export for SEO: title, description, keywords related to furniture company story
- Import necessary components
- Plan sections: Hero, Company Story, Values, Team (optional), Showroom Info

**About Hero Section:**
- Large headline: "About Sony Interior" or "Our Story"
- Background image: showroom interior or craftsmanship photo from Unsplash
- Breadcrumb navigation: Home > About
- Minimal design letting image speak
- Subtle entrance animation for headline

**Company Story Section:**
- Two or three paragraphs about Sony Interior's history, mission, design philosophy
- User will write actual copy later so include Lorem ipsum placeholder text
- Store this text in lib/data/about-content.ts file as exported constant
- Import and map in the component
- Include pull quote or highlighted text for visual interest
- Side image showing furniture being crafted or showroom
- Responsive layout: text and image side by side on desktop, stacked on mobile

**Values or Philosophy Section:**
- Grid of value cards: Quality Craftsmanship, Sustainable Materials, Timeless Design, Customer-Centric
- Each card: icon, headline, description paragraph
- Clean card design with subtle borders or shadows
- Grid: two columns on tablet, one on mobile, four on large desktop
- Icons can be from Lucide React or similar icon library
- Entrance animation as cards scroll into view

**Showroom Location Section:**
- Headline: "Visit Our Showroom"
- Placeholder for map that user will add later
- Reserve space with appropriate height for embedded map
- Address and contact information displayed prominently
- Opening hours if applicable
- CTA button: "Get Directions" which will link to map app later
- Store this information in lib/data/about-content.ts as well

**Page Polish:**
- Ensure all text is in variables imported from lib/data folder
- Add proper spacing between sections
- Implement scroll animations using Framer Motion or GSAP
- Test responsive behavior on all breakpoints
- Verify accessibility with proper heading hierarchy
- Add loading states if any dynamic content

---

## PHASE 6: Sanity CMS Integration

### Goals
Connect Next.js application to Sanity CMS for all product data management. Set up proper TypeScript interfaces, GROQ queries, and data fetching functions.

### Understanding Sanity Integration

**What You're Building:**
- Client configuration to connect to Sanity project
- TypeScript interfaces matching Sanity schema structure
- GROQ query strings for different data needs
- Data fetching functions with proper error handling
- Image URL builder for optimized image delivery

**Data Flow:**
- Products page fetches all products from Sanity
- Product detail pages fetch single product by slug
- Homepage fetches featured products
- All fetching happens server-side for SEO benefits

### Tasks

**Install Sanity Packages:**
- Install next-sanity package using pnpm add next-sanity
- Install @sanity/image-url for image optimization
- These packages provide client and image URL builder utilities

**Create Sanity Client Configuration:**
- Create new file: lib/sanity/client.ts
- Import createClient from next-sanity
- Configure client with projectId from NEXT_PUBLIC_SANITY_PROJECT_ID
- Set dataset from NEXT_PUBLIC_SANITY_DATASET
- Set apiVersion to today's date in format YYYY-MM-DD
- Set useCdn to true for faster read performance
- For authenticated requests create second client with token from SANITY_API_TOKEN
- Export both clients: one for public read, one for authenticated operations

**Create Image URL Builder:**
- In same file or new lib/sanity/image.ts
- Import imageUrlBuilder from @sanity/image-url
- Create builder instance with your client configuration
- Export helper function that takes Sanity image source and returns URL builder
- This will be used throughout app for optimized responsive images

**Define TypeScript Interfaces:**
- Create lib/types/sanity.ts file
- Define Product interface with fields:
  - id: string
  - name: string
  - slug: object with current: string
  - description: array (portable text)
  - price: number
  - compareAtPrice: optional number for sale prices
  - category: string or reference to category
  - dimensions: object with width, height, depth
  - materials: array of strings
  - colors: array of color objects
  - images: array of Sanity image objects
  - mainImage: Sanity image object for primary photo
  - stockStatus: string (in-stock, low-stock, out-of-stock)
  - featured: boolean
  - metadata: object with seo fields (title, description, keywords)
- Define SanityImage interface:
  - asset: reference object
  - alt: string
  - hotspot: optional object
  - crop: optional object
- Define Category interface if using category documents
- Export all interfaces for use throughout application

**Create GROQ Query Strings:**
- Create lib/sanity/queries.ts file
- Write query for all products: select all documents of type product, project relevant fields, include image assets
- Write query for single product by slug: filter by slug.current, include all fields, dereference related data
- Write query for featured products: filter where featured is true, limit to six or eight results
- Write query for products by category: filter by category field, allow passing category parameter
- Write query for product slugs: needed for generateStaticParams, just return slug values
- Each query should explicitly project fields rather than returning everything for performance
- Include image asset references with proper projection

**Create Data Fetching Functions:**
- Create lib/sanity/queries.ts or lib/sanity/fetch.ts file
- Import client and query strings
- Write getAllProducts async function: executes GROQ query, returns typed Product array, handles errors with try-catch
- Write getProductBySlug async function: takes slug parameter, returns single Product or null, handles not found case
- Write getFeaturedProducts async function: returns Product array of featured items
- Write getProductsByCategory async function: takes category parameter, returns filtered products
- Write getAllProductSlugs function: returns array of slug strings for static generation
- Each function should have proper TypeScript return types
- Add error logging but don't expose errors to client
- Consider caching strategies: use Next.js cache with appropriate revalidation times

**Test Data Fetching:**
- User will populate Sanity with sample products separately
- Once data exists, test each fetching function works correctly
- Verify images load from Sanity CDN
- Check that rich text description renders properly
- Ensure TypeScript types match actual data structure
- Handle cases where optional fields might be missing

---

## PHASE 7: Products Page and Individual Product Pages

### Goals
Create the main products listing page showing all furniture and individual product detail pages with full information and purchase options.

### Tasks

**Products Page Structure:**
- Create app/products/page.tsx file
- Add metadata export with SEO-optimized title and description
- Plan layout: filters sidebar on left (optional), product grid on right
- Import getAllProducts function from Sanity queries
- Fetch products data in server component

**Products Grid Display:**
- Display products in responsive grid: four columns desktop (xl:grid-cols-4), three tablet (md:grid-cols-3), two mobile (grid-cols-2)
- Each product card component:
  - Product image with proper aspect ratio
  - Product name below image
  - Price displayed clearly
  - Quick shop or view details button
  - Optional: sale badge if compareAtPrice exists and is higher than price
- Card hover effects: image zooms, shadow appears, button becomes more prominent
- Link entire card to product detail page: /products/[slug]
- Use Sanity image URL builder for optimized responsive images
- Add loading skeleton UI while products fetch

**Category Filtering (Optional Enhancement):**
- If implementing filters, add sidebar or top bar with category buttons
- Use URL search params to track selected category
- Filter products array based on selected category
- Update URL without page reload using Next.js navigation
- Show active filter state visually

**Empty State Handling:**
- If no products returned from Sanity, show friendly message
- Provide link back to homepage or contact
- Ensure doesn't break page layout

**Individual Product Pages Setup:**
- Create app/products/[slug]/page.tsx file for dynamic routes
- Export generateStaticParams function using getAllProductSlugs
- Export generateMetadata function using product data for SEO
- Import getProductBySlug function

**Product Detail Page Layout:**
- Two-column layout on desktop: images left, product info right
- Image gallery: main large image with thumbnail strip below
- Allow clicking thumbnails to change main image
- Implement image zoom on hover or click (optional enhancement)
- Use Sanity image URL builder with different sizes for thumbnails vs main image

**Product Information Display:**
- Product name as h1 heading
- Price prominently displayed, show compare at price if on sale
- Stock status indicator with appropriate styling
- Product description rendered from portable text (may need @portabletext/react package)
- Dimensions section showing width, height, depth
- Materials list
- Color options if applicable
- Add to cart button (functionality comes later, just UI for now)
- Quantity selector input
- Share buttons for social media (optional)

**Related Products Section:**
- At bottom of product page show related products
- Query products from same category excluding current product
- Display in horizontal scrolling row or grid
- Limit to four to six products
- Use same product card component as products page

**Mobile Responsiveness:**
- Stack images and info vertically on mobile
- Image gallery becomes swipeable carousel
- Ensure all text remains readable
- Buttons and inputs are touch-friendly
- Test on various mobile viewport sizes

**Not Found Handling:**
- If product slug doesn't exist, show not found UI
- Use Next.js notFound() function from next/navigation
- Create app/products/[slug]/not-found.tsx for custom 404 page
- Provide link to products page or homepage

---

## PHASE 8: Contact Page with Map Integration

### Goals
Create contact page with showroom location map, contact form, and business information.

### Tasks

**Contact Page Structure:**
- Create app/contact/page.tsx file
- Add metadata export for SEO
- Plan two-column layout: contact form left, map and info right
- On mobile: stack vertically with form on top

**Contact Form:**
- Form fields: name (text input), email (email input), phone (tel input, optional), subject (text input), message (textarea)
- Each field with proper label and placeholder
- Use controlled components with React state or form library like react-hook-form
- Add client-side validation for required fields and email format
- Submit button with loading state
- Form submission will connect to API later, for now just UI
- Success and error message display areas
- Ensure accessible form labels and ARIA attributes
- Style inputs consistently with design system

**Map Section:**
- Reserve space for embedded map (user will add actual map code later)
- Use appropriate height: 400-500px
- Add placeholder div with background color and text: "Map will be embedded here"
- Include comment noting user will add Google Maps iframe or similar
- Ensure responsive: full width on mobile

**Business Information Display:**
- Company name and logo
- Physical address of showroom formatted nicely
- Phone number with tel link for mobile calling
- Email address with mailto link
- Business hours if applicable
- Store this information in lib/data/contact-info.ts file
- Import and display in component
- Use icons from Lucide React for visual enhancement

**Page Styling:**
- Use design system colors and typography
- Add appropriate spacing between elements
- Subtle entrance animations using Framer Motion
- Ensure form is visually balanced with map section
- Test responsive behavior thoroughly

---

## PHASE 9: Python FastAPI Backend Setup

### Goals
Set up Python FastAPI backend that will handle RAG operations, embeddings, and host the OpenAI Agent SDK with LiteLLM routing to Gemini.

### Understanding Backend Purpose

**What This Backend Does:**
- Hosts the AI agent using OpenAI Agent SDK routed through LiteLLM
- Generates embeddings for product descriptions and content
- Stores embeddings in Neon Postgres with pgvector
- Performs vector similarity search for RAG
- Manages chat sessions and message history
- Provides REST API endpoints for Next.js frontend
- Handles user text selection embedding and search

### Tasks

**Project Structure Creation:**
- Create backend folder at project root (same level as src)
- Inside backend create:
  - main.py file as application entry point
  - routers folder for organizing endpoints
  - services folder for business logic
  - database folder for database operations
  - models folder for Pydantic schemas
  - utils folder for helper functions
  - requirements.txt for dependencies
  - .env file linking to root .env.local (or separate .env)

**Python Dependencies:**
- Create requirements.txt file with these packages:
  - fastapi - web framework
  - uvicorn[standard] - ASGI server
  - openai-agents - the OpenAI Agent SDK
  - litellm - for routing to Gemini
  - psycopg2-binary or asyncpg - Postgres adapter
  - pgvector - vector extension support
  - sentence-transformers - for generating embeddings
  - pydantic - data validation
  - python-dotenv - environment variables
  - httpx - HTTP client for API calls
  - python-multipart - form data handling

**Initialize Virtual Environment:**
- In backend folder create Python virtual environment
- Activate virtual environment
- Run pip install -r requirements.txt to install all dependencies
- Verify installations successful

**Main Application Setup:**
- In main.py import FastAPI
- Create FastAPI application instance
- Configure CORS to allow requests from Next.js frontend at localhost:3000
- Set up application startup and shutdown events
- Configure middleware for logging and error handling
- Define root endpoint that returns API status

**Database Connection Module:**
- In database folder create connection.py file
- Import necessary Postgres adapter
- Create connection pool using DATABASE_URL environment variable
- Export get_db function for dependency injection
- Handle connection errors gracefully
- Create pgvector extension enable function

**Run Development Server:**
- Create startup script or use uvicorn command
- Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
- Verify server starts without errors
- Test root endpoint returns expected response
- Check CORS headers allow Next.js origin

---

## PHASE 10: Database Schema Implementation

### Goals
Create database tables in Neon Postgres for chat history, embeddings storage, and user interactions.

### Tasks

**Enable pgvector Extension:**
- Connect to Neon database using psql or database GUI
- Run SQL command: CREATE EXTENSION IF NOT EXISTS vector;
- Verify extension is enabled
- This allows vector column type for embeddings

**Create Migrations:**
- In backend/database folder create migrations subfolder
- Create 001_initial_schema.sql file

**Chat Sessions Table:**
- Write CREATE TABLE statement for chat_sessions
- Columns: session_id (UUID PRIMARY KEY), created_at (TIMESTAMP), updated_at (TIMESTAMP), user_agent (TEXT), current_page (TEXT), metadata (JSONB)
- Add indexes on created_at for time-based queries

**Chat Messages Table:**
- Write CREATE TABLE for chat_messages
- Columns: message_id (UUID PRIMARY KEY), session_id (UUID FOREIGN KEY), role (VARCHAR), content (TEXT), created_at (TIMESTAMP), token_usage (INTEGER), page_context (TEXT)
- Add index on session_id for fast conversation retrieval
- Add foreign key constraint referencing chat_sessions

**Document Embeddings Table:**
- Write CREATE TABLE for document_embeddings
- Columns: embedding_id (UUID PRIMARY KEY), source_type (VARCHAR), source_id (TEXT), content_chunk (TEXT), embedding (VECTOR), metadata (JSONB), created_at (TIMESTAMP)
- The embedding column type is VECTOR with dimension matching your embedding model (384 for MiniLM, 1536 for OpenAI)
- Create vector index for fast similarity search: CREATE INDEX ON document_embeddings USING ivfflat (embedding vector_cosine_ops);
- Add indexes on source_type and source_id for filtering

**User Text Selections Table:**
- Write CREATE TABLE for user_text_selections
- Columns: selection_id (UUID PRIMARY KEY), session_id (UUID FOREIGN KEY), selected_text (TEXT), page_url (TEXT), created_at (TIMESTAMP), embedding (VECTOR optional)
- Add index on session_id

**Execute Migrations:**
- Connect to Neon database
- Execute migration SQL file
- Verify all tables created successfully
- Check indexes exist
- Test inserting sample data to verify schema works

**Create Database Helper Functions:**
- In backend/database folder create operations.py file
- Write async function to insert chat session: takes session data, returns session_id
- Write async function to insert chat message: takes message data, links to session
- Write async function to insert embedding: takes content, vector, metadata
- Write async function for vector similarity search: takes query vector, returns top K similar chunks
- Write async function to get chat history: takes session_id, returns messages array
- Each function should use connection pool and handle errors

---

## PHASE 11: Embeddings and RAG Implementation

### Goals
Implement embedding generation for products and content, store in database, and create vector similarity search for RAG retrieval.

### Understanding Embeddings

**What You're Building:**
- System to convert text into vector embeddings
- Storage of these vectors in Neon with pgvector
- Similarity search to find relevant content for user questions
- This powers the RAG (Retrieval-Augmented Generation) chatbot

**Embedding Strategy:**
- Embed product descriptions, specifications, dimensions info
- Embed website content like about page, policies, FAQ
- Chunk long content for better retrieval accuracy
- Store metadata with each embedding for filtering

### Tasks

**Choose Embedding Model:**
- Decide between sentence-transformers locally or OpenAI API
- For local: use all-MiniLM-L6-v2 model (384 dimensions, fast, good quality)
- For API: use OpenAI text-embedding-ada-002 (1536 dimensions, requires API key)
- Local is recommended for this project to reduce costs

**Create Embeddings Service:**
- In backend/services folder create embeddings.py file
- If using sentence-transformers: import SentenceTransformer, load model in class initialization
- Create generate_embedding function: takes text string, returns vector array
- Create batch_generate_embeddings function: takes list of texts, returns list of vectors
- Handle model loading and caching efficiently
- Add error handling for empty or invalid text

**Content Chunking Strategy:**
- Create chunking function that splits long text into overlapping segments
- Chunk size: 200-400 words depending on content type
- Overlap: 50-100 words between chunks for context continuity
- Special handling for product data: combine name, description, specifications into chunks
- Preserve metadata: which product or page each chunk came from

**Product Embedding Pipeline:**
- Create script or function to embed all Sanity products
- Fetch products from Sanity through Next.js API or directly if you have credentials
- For each product: combine name, description, category, materials into text
- Generate embedding for this combined text
- Store in document_embeddings table with source_type='product', source_id=product_id
- Handle products with missing fields gracefully
- Run this as initial data loading and on product updates

**Content Embedding Pipeline:**
- Manually prepare text content from About page, policies, FAQ
- Store source content in text files or Python strings
- Chunk longer content appropriately
- Generate embeddings for each chunk
- Store with source_type='page_content', source_id=page_slug
- This gives chatbot context about company and policies

**Vector Similarity Search:**
- In embeddings service create search_similar function
- Takes query embedding vector and optional filters
- Performs cosine similarity search in database
- Uses SQL with pgvector operators for efficient search
- Returns top K results (default K=5) with similarity scores
- Include the actual text content and metadata in results
- Filter by source_type if needed (only products, only content, etc.)

**RAG Context Assembly:**
- Create function that takes user question
- Generate embedding for the question
- Search for similar document chunks
- Format results into context string for LLM
- Include source attribution (which product or page)
- Limit total context length to fit in LLM context window
- Return formatted context ready for agent instructions

---

## PHASE 12: MCP Server Development

### Goals
Create Model Context Protocol servers that provide the AI agent with real-time access to Sanity products and Neon database without needing pre-embedded data.

### Understanding MCP Architecture

**What MCP Provides:**
- Direct real-time data access for the agent
- Tools that agent can call on-demand
- No need for stale embeddings for structured queries
- Better for deterministic questions like "What's the price of X sofa?"
- Complements RAG which is better for semantic search

**Your MCP Servers:**
- Sanity MCP Server: Exposes tools to query products by name, category, ID
- Database MCP Server: Exposes tools to query inventory, check stock, get order history (future)

### Tasks

**MCP Server Framework Setup:**
- Create mcp_servers folder at project root (sibling to backend and src)
- Inside create two subfolders: sanity_server and database_server
- Each will be standalone Python application
- Install MCP SDK if available or create custom HTTP server
- Alternative: Use function tools pattern directly in FastAPI

**Sanity MCP Server:**
- In sanity_server folder create main.py
- Define tool: search_products_by_name - takes product name string, returns matching products from Sanity
- Define tool: get_product_by_id - takes product ID, returns full product details
- Define tool: get_products_by_category - takes category name, returns products in that category
- Define tool: search_products_by_filter - takes flexible filters like price range, material, returns matching products
- Each tool makes GROQ query to Sanity API
- Use Sanity API token from environment
- Return data in structured format agent can understand
- Run this as HTTP server on port 3001

**Database MCP Server:**
- In database_server folder create main.py
- Define tool: check_product_stock - takes product ID, returns stock status from cache table
- Define tool: get_chat_history - takes session ID, returns previous messages
- Define tool: search_similar_content - takes query text, performs RAG vector search, returns results
- Each tool connects to Neon database
- Use DATABASE_URL from environment
- Return structured responses
- Run this as HTTP server on port 3002

**MCP Server Startup:**
- Create startup scripts for both servers
- They should run alongside FastAPI backend
- Configure to restart on crash
- Log requests and errors
- Add health check endpoints

**Integration with Agent:**
- MCP tools will be called by agent via HTTP requests
- FastAPI backend orchestrates calls to MCP servers
- Agent decides which tool to use based on user question
- Results flow back to agent for response generation

---

## PHASE 13: OpenAI Agent SDK Implementation with LiteLLM

### Goals
Implement the core AI agent using OpenAI Agent SDK routed through LiteLLM to Gemini, define tools, and create agent logic for handling furniture queries.

### CRITICAL: Follow User's Example Pattern

**Required Imports and Setup:**
- Import Agent, Runner, function_tool, set_tracing_disabled from agents package
- Import LitellmModel from agents.extensions.models.litellm_model
- Use async/await pattern with Runner.run() exactly as shown in example
- Set tracing disabled to reduce overhead
- Model string: gemini/gemini-2.0-flash or gemini/gemini-2.5-flash

### Tasks

**Create Agent Module:**
- In backend/services folder create agent.py file
- Import all necessary components from agents package
- Import LitellmModel for Gemini routing
- Load GEMINI_API_KEY from environment variables
- Define MODEL constant as 'gemini/gemini-2.5-flash'
- Call set_tracing_disabled(disabled=True) at module level

**Define Agent Tools Using function_tool Decorator:**

Each tool must use the @function_tool decorator pattern:

**Tool: search_products**
- Decorator: @function_tool
- Parameters: query (string), category (optional string)
- Function: Calls MCP Sanity server to search products
- Returns: List of matching products with names, prices, IDs
- Agent uses this when user asks about product availability

**Tool: get_product_details**
- Decorator: @function_tool
- Parameters: product_id (string)
- Function: Calls MCP Sanity server for full product information
- Returns: Complete product data including description, specs, pricing
- Agent uses this for detailed product questions

**Tool: search_similar_content**
- Decorator: @function_tool
- Parameters: query (string)
- Function: Calls Database MCP server for RAG vector search
- Returns: Relevant content chunks from embeddings
- Agent uses this for general knowledge questions about company or policies

**Tool: check_inventory**
- Decorator: @function_tool
- Parameters: product_id (string)
- Function: Calls Database MCP server to check stock
- Returns: Stock status string
- Agent uses when user asks about availability

**Tool: analyze_user_selection**
- Decorator: @function_tool
- Parameters: selected_text (string), page_context (string)
- Function: Generates embedding, searches for relevant info
- Returns: Information specifically about the selected text
- Agent uses when user highlights text and asks question

**Create Main Agent Function:**
- Define async function create_furniture_agent that returns configured Agent
- Agent configuration:
  - name: "Sony Interior Assistant"
  - instructions: Detailed prompt about being furniture expert, helping customers, using tools appropriately, staying on topic
  - model: LitellmModel(model=MODEL, api_key=gemini_api_key)
  - tools: List of all function_tool decorated tools defined above
- Instructions should specify: only answer furniture-related questions, use tools before responding, provide product recommendations, be friendly and professional
- Return the configured Agent instance

**Create Agent Runner Function:**
- Define async function run_agent_query
- Parameters: user_message (string), session_context (dict with page_url, selected_text if any)
- Inside function: call create_furniture_agent to get agent instance
- Augment user_message with session context info
- Call: result = await Runner.run(agent, augmented_message)
- Extract result.final_output
- Return agent response as string
- Handle any errors with try-except and return error message

**Agent Instructions Refinement:**
- Instructions should guide agent behavior:
  - "You are Sony Interior's virtual furniture consultant"
  - "Help customers find perfect furniture for their needs"
  - "Use search_products tool to find items matching customer requests"
  - "Use get_product_details for specific product questions"
  - "Use search_similar_content for company information or policies"
  - "Always be friendly, helpful, and professional"
  - "If question is not about furniture or Sony Interior, politely redirect"
  - "Provide recommendations based on user preferences"
  - "Format responses with clear product names and prices"

**Test Agent Locally:**
- Create test script that imports agent module
- Call run_agent_query with sample questions
- Verify tools are being called appropriately
- Check responses are relevant and well-formatted
- Test error handling with invalid inputs
- Ensure Gemini API calls work through LiteLLM

---

## PHASE 14: FastAPI Chat Endpoint

### Goals
Create FastAPI endpoint that receives chat messages from Next.js frontend, runs the agent, and streams responses back.

### Tasks

**Create Chat Router:**
- In backend/routers folder create chat.py file
- Import APIRouter from FastAPI
- Create router instance
- Import agent functions from services
- Import database operations for storing messages

**Define Request/Response Models:**
- In backend/models folder create chat_models.py
- Define Pydantic model ChatRequest with fields:
  - message: str (user's message)
  - session_id: str (chat session identifier)
  - page_context: Optional[str] (current page URL)
  - selected_text: Optional[str] (text user highlighted)
- Define ChatResponse model with fields:
  - response: str (agent's reply)
  - session_id: str
  - sources: Optional[List] (products or content sources used)

**Implement Chat Endpoint:**
- Create POST endpoint at /api/chat
- Accept ChatRequest in request body
- Extract message, session_id, context from request
- Check if session exists in database, create if new
- Store user message in chat_messages table
- Build context dict with page and selected text info
- Call run_agent_query function with message and context
- Wait for agent response
- Store agent response in chat_messages table
- Extract any source references from agent's tool usage
- Return ChatResponse with agent reply and sources
- Handle errors gracefully and return appropriate status codes

**Add Streaming Support (Optional Enhancement):**
- If you want to stream responses token by token
- Use FastAPI StreamingResponse
- Modify agent to yield chunks instead of waiting for complete response
- Frontend can display words as they arrive
- More complex but better user experience

**Session Management:**
- Create helper function to get or create session
- Generate UUID for new sessions
- Store session metadata (user_agent, initial page)
- Track session updated_at timestamp
- Allow retrieving full conversation history by session_id

**Rate Limiting:**
- Add rate limiting to prevent abuse
- Limit requests per session or IP address
- Return 429 status code if limit exceeded
- Clear rate limits periodically

**Mount Router in Main:**
- In main.py import chat router
- Include router with prefix /api
- Now endpoint accessible at localhost:8000/api/chat

---

## PHASE 15: Quick Questions Feature

### Goals
Implement system that generates contextual quick questions based on current page that users can click to ask the chatbot.

### Understanding Quick Questions

**What They Are:**
- Short pre-generated questions relevant to current page
- Displayed as clickable pills in chatbot interface
- When clicked, automatically send question to agent
- Makes chatbot more discoverable and easier to use

**Examples:**
- On product page: "What are the dimensions?", "Is this in stock?", "Show me similar items"
- On homepage: "What's new this month?", "Tell me about your bestsellers"
- On about page: "Where is your showroom?", "What makes your furniture special?"

### Tasks

**Create Quick Questions Generator:**
- In backend/services create quick_questions.py file
- Define function generate_quick_questions
- Parameters: page_type (string), page_context (dict with relevant info)
- Returns: List of 3-5 question strings
- Use simple rule-based logic initially:
  - If page_type is "product": return product-specific questions
  - If page_type is "products": return browsing-related questions
  - If page_type is "home": return general discovery questions
  - If page_type is "about": return company info questions
  - If page_type is "contact": return support questions

**Product Page Questions:**
- "What are the dimensions of this item?"
- "Is this currently in stock?"
- "What materials is this made from?"
- "Show me similar products"
- "What's the price and any current deals?"

**Products Listing Questions:**
- "What are your bestselling items?"
- "Show me sofas under $1000"
- "What new products arrived recently?"
- "Help me find a dining table"
- "What furniture categories do you offer?"

**Homepage Questions:**
- "What makes Sony Interior unique?"
- "Tell me about your featured collection"
- "How can I visit your showroom?"
- "What's your return policy?"

**About Page Questions:**
- "Where are you located?"
- "Tell me about your craftsmanship"
- "What's your sustainability approach?"
- "How long have you been in business?"

**Create API Endpoint:**
- In chat router add GET endpoint /api/quick-questions
- Accept query parameters: page_type and optionally product_id
- Call generate_quick_questions function
- Return JSON array of question strings
- Cache results briefly to reduce computation

**Frontend Integration Plan:**
- Next.js will call this endpoint when page loads or changes
- Display questions as clickable buttons in chat widget
- On click, send question as if user typed it
- Hide/show questions based on chat state

**Enhanced Version with LLM:**
- For better questions, use agent to generate them
- Call LiteLLM directly with prompt: "Generate 3 relevant questions a user might ask about [page context]"
- Parse response into question list
- This creates more natural, contextual questions
- Can reference specific product details dynamically

---

## PHASE 16: Frontend Chat Integration with Vercel AI SDK

### Goals
Connect Next.js frontend to Python backend, implement chat UI using Vercel AI SDK's useChat hook, handle streaming responses, and display messages beautifully.

### Understanding Vercel AI SDK Frontend

**What useChat Provides:**
- Messages state array with all conversation messages
- Input value and handleInputChange for textarea
- handleSubmit function for sending messages
- isLoading state during agent processing
- Automatic message ID generation
- Error handling

### Tasks

**Install Frontend Dependencies:**
- Ensure ai and @ai-sdk/react packages are installed
- These provide useChat hook and related utilities

**Create Next.js API Route Proxy:**
- Create app/api/chat/route.ts file
- This proxies requests from frontend to Python backend
- Import necessary Next.js types
- Define POST handler
- Extract message and context from request body
- Make fetch call to Python backend at PYTHON_BACKEND_URL/api/chat
- Forward request body
- Stream response back to frontend
- Handle errors and return appropriate responses
- This separation allows Python to handle AI logic while Next.js handles routing

**Update ChatWidget Component:**
- Open existing src/components/ChatWidget.tsx
- Import useChat from ai/react package
- Import useState, useEffect for additional state
- Call useChat hook with API endpoint: /api/chat
- Destructure messages, input, handleInputChange, handleSubmit, isLoading from hook

**Chat UI Structure:**
- Floating widget button in bottom right corner
- On click: widget expands to show chat interface
- Chat interface: header with title and close button, messages container, input area at bottom
- Header: "Sony Interior Assistant" with minimize/close icon
- Messages area: scrollable div displaying all messages
- Each message shows role (user or assistant) and content
- User messages aligned right with different background
- Assistant messages aligned left with different background
- Input area: textarea for typing, send button, quick questions below

**Message Rendering:**
- Map over messages array from useChat
- Display each message with appropriate styling based on role
- User messages: blue/accent background, white text, right-aligned
- Assistant messages: light gray background, dark text, left-aligned
- Add avatar icons: user icon for human, bot icon for assistant
- Format timestamps if available
- Handle markdown in assistant messages if they use formatting
- Auto-scroll to bottom when new messages arrive

**Input Handling:**
- Textarea for message input
- Bind value to input from useChat
- Bind onChange to handleInputChange
- On Enter key (without Shift): call handleSubmit
- On Shift+Enter: allow new line
- Send button next to textarea
- Disable input and button when isLoading is true
- Show typing indicator when agent is responding

**Quick Questions Integration:**
- Fetch quick questions from /api/quick-questions on widget open
- Pass current page path as page_type parameter
- Display questions as clickable pill buttons
- On click: set input value to question text and call handleSubmit
- Hide quick questions after first user message or show fresh ones
- Loading state while fetching questions

**Page Context Tracking:**
- Use Next.js usePathname hook to get current page
- Include page URL in chat request context
- Update when page changes
- This helps agent provide relevant responses

**Text Selection Feature:**
- Add event listener for text selection on page
- When user highlights text and clicks chat icon or uses context menu
- Capture selected text
- Send with next chat message as selected_text in context
- Agent can then answer specifically about that text
- Show indicator in chat when selection is active
- Clear selection after use

**Widget State Management:**
- Track open/closed state with useState
- Track minimized/expanded state
- Persist open state in localStorage (optional)
- Smooth animations for opening/closing using Framer Motion
- Slide in from bottom right corner
- Fade in overlay if using backdrop

**Error Handling:**
- Display error messages if API call fails
- Show retry button
- Don't break UI on errors
- Log errors to console for debugging

**Mobile Responsiveness:**
- On mobile: widget takes full screen or bottom sheet
- Ensure input doesn't get hidden by keyboard
- Adjust layout for smaller screens
- Make close/minimize buttons touch-friendly

---

## PHASE 17: UI Polish and Animations

### Goals
Add final polish with smooth animations using GSAP and Framer Motion, ensure excellent mobile experience, and optimize performance.

### Tasks

**Hero Section GSAP Animations:**
- In Hero component use GSAP for entrance animations
- Create timeline: headline fades in and slides up from bottom
- Stagger subheadline and CTA button with delays
- Add parallax effect on background image with ScrollTrigger
- On mobile: simplify animations for performance
- Ensure animations only run once per page load

**Product Card Animations:**
- Use Framer Motion for product card hover effects
- Scale image on hover: scale from 1 to 1.05
- Add shadow on hover using shadow prop
- Stagger product cards entrance when section comes into view
- Use InView component from Framer Motion to trigger
- Each card animates with slight delay creating wave effect

**Scroll Animations:**
- Identify sections that should animate on scroll
- Use GSAP ScrollTrigger or Framer Motion InView
- Fade in and slide up sections as they enter viewport
- Pin certain sections briefly (optional advanced effect)
- Smooth scroll behavior using Lenis if not already implemented
- Test scroll performance on various devices

**Page Transitions:**
- Add page transition animations between routes
- Use Framer Motion AnimatePresence in layout
- Fade out current page, fade in next page
- Keep transitions subtle and fast (200-300ms)
- Ensure doesn't interfere with browser back/forward

**Chat Widget Animations:**
- Slide in animation when widget opens
- Message bubble entrance animations
- Typing indicator with animated dots
- Smooth auto-scroll when new messages arrive
- Button hover and press states with scale transforms

**Mobile Optimization:**
- Test all animations on mobile devices
- Reduce or disable complex animations on low-end devices
- Check for jank or stuttering
- Ensure touch interactions feel responsive
- Optimize images for mobile viewport sizes

**Performance Optimization:**
- Use will-change CSS for animated elements
- Lazy load images below fold
- Code split heavy components
- Minimize JavaScript bundle size
- Use Next.js Image component for all images
- Enable Tailwind CSS JIT mode if not already
- Remove unused Tailwind classes in production

**Accessibility:**
- Add prefers-reduced-motion media query
- Disable animations if user has motion sensitivity
- Ensure keyboard navigation works throughout
- Check color contrast ratios meet WCAG standards
- Add ARIA labels where needed
- Test with screen readers

**Cross-Browser Testing:**
- Test on Chrome, Firefox, Safari, Edge
- Verify animations work consistently
- Check for vendor prefix requirements
- Test on iOS Safari and Android Chrome
- Fix any browser-specific issues

---

## PHASE 18: Testing, Debugging, and Documentation

### Goals
Thoroughly test all functionality, fix bugs, optimize performance, and document the codebase for maintenance.

### Tasks

**Functionality Testing:**
- Test all pages load correctly
- Verify Sanity product data displays properly
- Test product filtering and search if implemented
- Check individual product pages render complete info
- Test contact form validation
- Verify chatbot responds to various questions
- Test quick questions feature
- Verify text selection feature works
- Check navigation works across all pages
- Test mobile navigation menu

**Chatbot Testing:**
- Ask questions about specific products
- Test category searches: "Show me dining tables"
- Ask about company info: "Tell me about Sony Interior"
- Test with selected text: highlight content and ask question
- Verify agent uses appropriate tools
- Check responses are accurate and relevant
- Test error handling with invalid queries
- Verify off-topic questions are redirected politely
- Test conversation flow with multiple messages
- Check session persistence works

**Performance Testing:**
- Use Lighthouse to check performance scores
- Optimize Core Web Vitals: LCP, FID, CLS
- Check page load times on slow connections
- Test with throttled CPU
- Identify and fix slow database queries
- Optimize image loading and sizes
- Check for memory leaks in animations
- Profile Python backend response times

**Error Handling:**
- Test with network failures
- Verify graceful degradation when APIs are down
- Check error messages are user-friendly
- Test with missing environment variables
- Verify database connection failures are handled
- Test with malformed user inputs
- Ensure errors don't expose sensitive info

**Security Considerations:**
- Never expose API keys in frontend code
- Validate all user inputs on backend
- Prevent SQL injection with parameterized queries
- Sanitize user messages before storing
- Rate limit API endpoints
- Add CSRF protection if needed
- Ensure CORS is properly configured
- Check for XSS vulnerabilities

**Code Documentation:**
- Add JSDoc comments to complex functions
- Document Sanity schema in README
- Explain GROQ queries with comments
- Document agent tools and their purposes
- Create API documentation for backend endpoints
- Add inline comments for non-obvious logic
- Update CLAUDE.md with any changes made

**README Creation:**
- Create comprehensive README.md file
- Include project overview and features
- List all environment variables needed
- Provide setup instructions step by step
- Document how to run development servers
- Explain project structure
- Add screenshots of key pages
- Include troubleshooting section

**Deployment Preparation:**
- Choose hosting: Vercel for Next.js, Railway/Render for Python
- Configure environment variables on hosting platforms
- Set up Neon database for production
- Update CORS settings for production domain
- Configure build commands and start scripts
- Test production builds locally
- Create deployment checklists

**Final Polishing:**
- Fix any console warnings
- Remove all console.log statements
- Ensure TypeScript has no errors
- Format code consistently
- Check all links work
- Verify images have proper alt text
- Test all animations one more time
- Get feedback from others if possible

---

## Phase Completion Notes

**Each phase should be completed fully before moving to next one. After completing each phase:**
- Test that everything works as expected
- Commit changes to version control
- Document any issues encountered
- Note any improvements needed for future

**The user will:**
- Populate Sanity with actual product data
- Write copy for About page and other text content
- Add actual showroom map to Contact page
- Configure environment variables with real keys
- Test and provide feedback

**You are building:**
- A beautiful, modern furniture website
- An intelligent AI chatbot powered by Gemini through LiteLLM
- A RAG system for accurate product information
- MCP servers for real-time data access
- A complete full-stack application following best practices

**Remember throughout:**
- Follow the user's example code pattern for OpenAI Agent SDK
- Use LiteLLM to route to Gemini, never use OpenAI keys
- Keep GSAP for complex animations
- Store text content in lib/data folder
- Store repeated CSS classes in globals.css
- Add metadata to every page
- Follow Next.js best practices
- Keep code clean, typed, and documented

Good luck with the build! 🚀
