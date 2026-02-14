---
name: frontend-dev
description: Frontend development best practices - React/Vue/HTML/CSS/JavaScript.
---

## HTML Best Practices
- Semantic tags (header/nav/main/article/section/footer)
- Images have alt attributes
- Keyboard navigable (tabindex, focus management)

## CSS Best Practices
- Prefer Flexbox/Grid layout
- Mobile-first (min-width media queries)
- CSS variables for theming
- Avoid deep selector nesting (max 3 levels)

## JavaScript Best Practices
- Prefer const, use let when needed, never var
- Async operations use async/await
- Error boundary handling
- Debounce/throttle high-frequency events

## React Specific
- Function components + Hooks
- Minimize state lifting
- useMemo/useCallback on-demand (don't over-optimize)
- key: use stable unique ID, not index

## Performance
- Lazy load images
- Code splitting (dynamic import)
- Virtual scrolling for long lists
- Avoid unnecessary re-renders
