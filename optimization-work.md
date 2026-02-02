# Next.js Performance Optimization Guide for Claude Code

This guide provides a systematic approach to review and optimize your Next.js project to achieve maximum performance scores (90-100). Follow these phases sequentially using pnpm for package management.

---

## Phase 1: Project Analysis & Baseline Assessment

### Objective: Understand the current state and identify all optimization opportunities

### Tasks:

1. **Scan the entire project structure**
   - List all pages in the app directory
   - Identify all component files
   - Map out the folder structure and organization
   - Note any files larger than 300 lines that need refactoring

2. **Review dependencies**
   - Examine package.json for heavy libraries
   - Identify any unused dependencies
   - Look for libraries that could be replaced with lighter alternatives or native APIs

3. **Search for common issues**
   - Count how many files use the "use client" directive
   - Find all instances of standard img tags
   - Locate any data fetching happening in layout files
   - Check for repeated data fetching patterns

4. **Install bundle analyzer if needed**
   - Add the Next.js bundle analyzer as a dev dependency using pnpm
   - Configure it to run when needed

5. **Document findings**
   - Create a checklist of all issues found
   - Prioritize issues based on impact
   - Create a backup branch before making changes

---

## Phase 2: Fix "use client" Directive Misuse

### Objective: Minimize JavaScript bundle size by removing unnecessary client components

### Decision Framework:

**Keep "use client" only when the component:**
- Uses React hooks like useState, useEffect, useContext, useReducer, useRef
- Has event handlers like onClick, onChange, onSubmit, onKeyDown
- Uses browser APIs like window, document, localStorage, sessionStorage
- Imports client-only libraries for animations, charts, or visualizations
- Uses Next.js client hooks like useRouter, usePathname, useSearchParams

**Remove "use client" when the component:**
- Only renders JSX without interactivity
- Just formats or displays data passed as props
- Performs calculations or transformations that don't need state
- Contains no event handlers or browser-specific code
- Fetches data that could be fetched on the server

### Implementation Steps:

1. **Create a list of all files with "use client"**
   - Search the entire app directory
   - Document each component's purpose

2. **Analyze each component individually**
   - Review what the component does
   - Check if it truly needs client-side features
   - Determine if it can be a server component

3. **Refactor components that don't need "use client"**
   - Simply remove the directive if no client features are used
   - For components with mixed logic, split them into separate server and client components
   - Keep static/presentational parts on the server
   - Extract interactive parts into small client components

4. **Test thoroughly after each change**
   - Ensure functionality remains intact
   - Verify no errors appear
   - Check that interactivity still works as expected

---

## Phase 3: Optimize All Images

### Objective: Replace all standard img tags with Next.js Image component for automatic optimization

### Steps:

1. **Find all image usages**
   - Search for all img tags in the project
   - Look for background images in CSS or Tailwind classes
   - Document the location and purpose of each image

2. **Replace standard img tags with Next.js Image component**
   - Import Image from next/image
   - Add appropriate width and height props
   - Set alt text for accessibility
   - Add className for styling if needed

3. **Optimize based on image purpose**
   - For hero images or logos above the fold, add the priority prop
   - For images below the fold, use lazy loading (default behavior)
   - For full-width responsive images, use the fill prop with proper parent styling
   - Adjust quality prop based on image importance (default is 75)

4. **Configure external image domains if needed**
   - If using images from CDNs or external sources, add them to next.config.js
   - Set up remote patterns for allowed domains

5. **Optimize source images**
   - Ensure images aren't unnecessarily large
   - Use appropriate dimensions for their display size
   - Prefer modern formats (Next.js handles conversion automatically)

---

## Phase 4: Replace Heavy Third-Party Libraries

### Objective: Reduce bundle size by eliminating or replacing heavy dependencies

### Steps:

1. **Analyze current bundle size**
   - Run the production build
   - Review the output to identify large chunks
   - Use the bundle analyzer for detailed breakdown

2. **Identify heavy libraries to replace**
   - Look for Moment.js and replace with native Intl API or date-fns
   - Check if Lodash is used and replace with native JavaScript methods
   - Review any other large libraries that might have lighter alternatives

3. **Replace Moment.js**
   - Remove the package using pnpm
   - For simple date formatting, use native Intl.DateTimeFormat
   - For relative time, use Intl.RelativeTimeFormat
   - If more features needed, install date-fns which is tree-shakeable

4. **Replace or optimize Lodash usage**
   - Remove full Lodash imports
   - Use native array methods, Set, Map, and Object methods
   - For debounce or specialized utilities, create small helper functions
   - If specific Lodash functions are truly needed, import them individually

5. **Dynamic import heavy components**
   - For rich text editors, charts, or visualization libraries, use dynamic imports
   - Load them only when needed
   - Disable server-side rendering for client-only components
   - Show loading states while importing

6. **Remove unused dependencies**
   - Install and run depcheck to find unused packages
   - Remove any packages that aren't being used
   - Clean up the package.json

---

## Phase 5: Implement Streaming with Suspense Boundaries

### Objective: Prevent slow data fetching from blocking the entire page render

### Concept:
Instead of waiting for all data before showing anything, render static parts immediately and stream in dynamic parts as they're ready.

### Steps:

1. **Identify pages with blocking data fetches**
   - Find pages that fetch data at the top level
   - Look for pages where everything waits for slow queries or API calls
   - Note pages with multiple independent data sources

2. **Implement Suspense boundaries around data-dependent sections**
   - Wrap components that fetch data with Suspense
   - Keep static elements like headers, navbars, and footers outside Suspense
   - Each independent data source can have its own Suspense boundary

3. **Create separate components for async data fetching**
   - Extract data fetching logic into dedicated async components
   - Each component fetches its own data
   - These components are wrapped in their own Suspense boundaries

4. **Design and implement loading skeletons**
   - Create skeleton components that match the layout of actual content
   - Use simple CSS animations for visual feedback
   - Make skeletons visually similar to final content for smooth transitions

5. **Use route-level loading states**
   - Create loading.tsx files in route directories
   - These automatically wrap the page in a Suspense boundary
   - Show appropriate loading UI for the entire route

6. **Fetch data in parallel when possible**
   - If multiple data sources are needed, fetch them simultaneously
   - Use Promise.all to wait for multiple async operations
   - This reduces total loading time compared to sequential fetching

---

## Phase 6: Optimize User Session Fetching in Layouts

### Objective: Prevent session fetching from forcing all child routes into dynamic rendering

### Problem:
Fetching user sessions in server-side layout components forces Next.js to dynamically render every page, preventing static optimization.

### Solution:
Move session handling to client-side components or use middleware.

### Steps:

1. **Find all session fetching in layout files**
   - Search layout files for getServerSession or similar calls
   - Document where session data is being used

2. **Refactor to client-side session handling**
   - Remove server-side session fetching from layouts
   - Install or configure your auth library's client-side provider
   - Wrap the application in the session provider at the root layout
   - Session provider should be a client component

3. **Create client components for session-dependent UI**
   - Build separate client components that fetch session data
   - Use the session on the client side with appropriate hooks
   - Show loading states while session loads
   - Handle unauthenticated states gracefully

4. **Move session logic from layouts to specific pages**
   - If only certain pages need session data, fetch it there instead of in the layout
   - This allows pages that don't need session to remain static

5. **Test that pages can be statically generated**
   - Check the build output to confirm pages are static
   - Verify that only pages with dynamic data requirements are marked as dynamic

---

## Phase 7: Use Middleware for Authentication

### Objective: Handle authentication at the edge without forcing pages into dynamic rendering

### Benefits:
- Authentication happens before reaching the server
- Pages can remain static
- Faster redirects
- Better performance and security

### Steps:

1. **Create a middleware file at the project root**
   - Create middleware.ts or middleware.js
   - This file runs before any page renders

2. **Implement authentication logic in middleware**
   - Check if user has a valid session token
   - Identify which routes require authentication
   - Identify which routes should be inaccessible when authenticated

3. **Handle redirects for protected routes**
   - If user is not authenticated and tries to access protected route, redirect to login
   - Preserve the intended destination for post-login redirect
   - Use URL parameters or session storage for return URLs

4. **Handle redirects for auth pages**
   - If user is already authenticated and visits login or register, redirect to dashboard
   - This prevents confusion and improves user experience

5. **Configure middleware matcher**
   - Specify which routes the middleware should run on
   - Include all protected routes
   - Include authentication pages
   - Exclude public assets and API routes that don't need auth

6. **Add role-based protection if needed**
   - Check user roles or permissions in middleware
   - Redirect unauthorized users to appropriate error pages
   - Keep authorization logic consistent

7. **Remove authentication logic from page components**
   - Delete server-side session checks from page files
   - Remove redirect logic from pages
   - Let middleware handle all authentication concerns

---

## Phase 8: Eliminate Repeated Data Fetching with React Cache

### Objective: Prevent the same data from being fetched multiple times during a single render

### Problem:
When multiple components need the same data (like user session or settings), they might each fetch it separately, causing redundant database queries or API calls.

### Solution:
Use React's cache function to memoize data fetching, ensuring each unique request happens only once per render pass.

### Steps:

1. **Identify repeated data fetching patterns**
   - Look for the same data fetching function called in multiple components
   - Common examples: user sessions, user profiles, settings, permissions
   - Check if multiple components are fetching the same data independently

2. **Wrap data fetching functions with React's cache**
   - Import cache from React
   - Wrap each data fetching function that might be called multiple times
   - The cache will ensure the function executes only once per render pass
   - All subsequent calls return the cached result

3. **Apply to common patterns**
   - Wrap functions that fetch user data
   - Cache settings and configuration fetching
   - Apply to any frequently accessed data across components
   - Include database queries that are called multiple times

4. **Use cached functions throughout the application**
   - Replace direct data fetching with calls to cached functions
   - Multiple components can now safely call the same function
   - Only one actual fetch will occur per request
   - All components get the same data without additional cost

5. **Understand cache scope**
   - Cache only works for one render pass (one request)
   - It doesn't persist between different requests
   - It's perfect for avoiding redundant fetches within a single page render
   - Different from client-side memoization or global caching

6. **Combine with Suspense for optimal results**
   - Use cached data fetching functions inside Suspense boundaries
   - Multiple components within the same Suspense can share cached data
   - This pattern gives you both streaming and efficient data fetching

---

## Phase 9: Code Refactoring & Component Organization

### Objective: Break down large files and eliminate code repetition for better maintainability and performance

### Steps:

1. **Identify files that are too large**
   - Find files with more than 300 lines of code
   - Focus especially on page files that have become monolithic
   - Look for files with multiple responsibilities

2. **Analyze the main page for refactoring opportunities**
   - Review the homepage or main landing page
   - Look for repeated patterns or similar code blocks
   - Identify distinct sections that could be separate components

3. **Extract repetitive elements into reusable components**
   - If the same JSX pattern appears multiple times, create a component
   - Replace repeated code with a single component and map over data
   - Create a data structure (array of objects) with the varying information
   - Map over the data to render multiple instances of the component

4. **Break large pages into section components**
   - Split the page into logical sections (hero, features, testimonials, pricing, etc.)
   - Create a separate component file for each major section
   - Import and compose these sections in the main page file
   - The main page becomes a clean composition of sections

5. **Create reusable UI components**
   - Identify common UI patterns like buttons, cards, inputs, modals
   - Build a library of reusable UI components with props for customization
   - Use these components consistently throughout the application
   - This reduces code duplication and ensures visual consistency

6. **Extract repeated logic into utility functions**
   - Find logic that's duplicated across components
   - Create utility functions in a lib or utils directory
   - Import and use these utilities wherever needed
   - Common examples: data formatting, API calls, validation logic

7. **Organize components into a clear folder structure**
   - Create folders for different types of components (UI, sections, features, layout)
   - Group related components together
   - Use clear, descriptive names for files and folders
   - Make it easy to find and maintain components

8. **Apply the DRY principle to data**
   - Move hardcoded data out of components
   - Create data files or constants for lists, configurations, content
   - Import data where needed rather than duplicating it
   - Makes updates easier and reduces errors

9. **Ensure components have single responsibilities**
   - Each component should do one thing well
   - If a component is doing too much, split it further
   - Smaller, focused components are easier to understand and maintain
   - They're also easier to optimize and test

---

## Phase 10: Final Optimization & Testing

### Objective: Verify all optimizations and measure performance improvements

### Steps:

1. **Run a production build**
   - Build the application for production
   - Review build output for any warnings or issues
   - Check that pages are being statically generated where expected
   - Verify bundle sizes are reasonable

2. **Analyze the bundle**
   - Use the bundle analyzer to see what's included
   - Ensure no unexpected large dependencies remain
   - Verify code splitting is working properly
   - Check that client components are appropriately sized

3. **Run Lighthouse audits**
   - Test on the homepage and other key pages
   - Run audits for mobile and desktop
   - Check all four metrics: Performance, Accessibility, Best Practices, SEO
   - Document the scores

4. **Test Core Web Vitals**
   - Measure Largest Contentful Paint (LCP)
   - Check First Input Delay (FID) or Interaction to Next Paint (INP)
   - Verify Cumulative Layout Shift (CLS)
   - Ensure all metrics are in the "good" range

5. **Verify functionality**
   - Test all interactive features
   - Ensure authentication works correctly
   - Check that data loads properly
   - Verify images display correctly
   - Test on different devices and browsers

6. **Test loading states**
   - Verify Suspense boundaries show appropriate loading UI
   - Check that skeletons display correctly
   - Ensure smooth transitions when data loads
   - Test with throttled network speeds

7. **Review and fix any remaining issues**
   - Address any warnings or errors from the build
   - Fix any Lighthouse recommendations
   - Optimize any metrics that aren't in the target range
   - Make incremental improvements

8. **Document the changes**
   - Create a summary of all optimizations made
   - Document before and after performance metrics
   - Note any patterns or practices to follow going forward
   - Share learnings with the team

9. **Set up performance monitoring**
   - Consider adding real user monitoring
   - Track Core Web Vitals in production
   - Set up alerts for performance regressions
   - Regularly audit performance as the site grows

---

## Phase 11: Ongoing Maintenance

### Objective: Maintain high performance as the project evolves

### Best Practices:

1. **Regular audits**
   - Run Lighthouse audits monthly or after major changes
   - Monitor bundle size with each deploy
   - Keep an eye on Core Web Vitals in production

2. **Code review checklist**
   - Before adding "use client", verify it's truly needed
   - Always use Next.js Image for images
   - Check if new dependencies are necessary and lightweight
   - Ensure new data fetching uses cache and Suspense appropriately

3. **Dependency management**
   - Regularly update dependencies to get performance improvements
   - Remove dependencies that are no longer needed
   - Evaluate new dependencies for size and necessity before adding

4. **Performance budget**
   - Set limits for bundle size
   - Set targets for Lighthouse scores
   - Set thresholds for Core Web Vitals
   - Reject changes that significantly regress performance

5. **Documentation**
   - Document performance patterns and anti-patterns
   - Keep this optimization guide updated
   - Share performance wins and learnings with the team
   - Make performance a shared responsibility

---

## Summary Checklist

Before considering optimization complete, verify:

- [ ] All unnecessary "use client" directives removed
- [ ] All images using Next.js Image component
- [ ] No heavy libraries like Moment.js in the bundle
- [ ] Suspense boundaries implemented for async data
- [ ] Session fetching moved to client components or middleware
- [ ] Middleware handling authentication for protected routes
- [ ] Data fetching functions wrapped with React cache
- [ ] Large files broken down into smaller components
- [ ] Repetitive code replaced with mapped components
- [ ] Production build runs successfully
- [ ] Lighthouse scores above 90 on key pages
- [ ] Core Web Vitals in "good" range
- [ ] All functionality tested and working
- [ ] Performance improvements documented

This systematic approach will help you achieve and maintain excellent performance scores while keeping the codebase clean and maintainable.