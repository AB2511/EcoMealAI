# Design Document

## Overview

This design addresses critical UI rendering issues in the EcoMeal AI application where HTML content is not properly rendered, icons display as text, graphs have poor contrast, and unwanted print features are visible. The solution involves creating a comprehensive HTML content filtering system, icon rendering fixes, graph text visibility improvements, and print media query management.

## Architecture

The solution follows a layered architecture approach:

1. **HTML Content Filter Layer**: Intercepts and processes raw HTML content before display
2. **Icon Rendering System**: Manages proper icon display and fallback mechanisms  
3. **Graph Text Visibility Manager**: Ensures readable text in all chart components
4. **Print Media Controller**: Manages print-specific styling and feature visibility

## Components and Interfaces

### 1. Enhanced HTML Content Filter

**Purpose**: Prevent raw HTML tags and code from displaying as text in the UI

**Key Components**:
- `CriticalHTMLContentFilter`: Main filtering class that processes content
- `StreamlitContentInterceptor`: Intercepts Streamlit display functions
- `IngredientListProcessor`: Specifically handles ingredient list HTML rendering

**Interface**:
```python
class CriticalHTMLContentFilter:
    def filter_html_content(self, content: str) -> str
    def process_ingredient_lists(self, html_content: str) -> dict
    def sanitize_display_content(self, content: Any) -> Any
    def apply_content_filtering(self) -> None
```

### 2. Icon Rendering System

**Purpose**: Fix icon display issues where text strings appear instead of visual icons

**Key Components**:
- `IconRenderingManager`: Manages icon display and fallback systems
- `SidebarIconFixer`: Specifically addresses sidebar navigation icon issues
- `MaterialIconLoader`: Loads and manages Material Design icons

**Interface**:
```python
class IconRenderingManager:
    def fix_sidebar_icons(self) -> None
    def load_material_icons(self) -> None
    def replace_text_with_icons(self, text: str) -> str
    def inject_icon_css(self) -> None
```

### 3. Graph Text Visibility Manager

**Purpose**: Ensure all text in dashboard graphs and charts is readable with proper contrast

**Key Components**:
- `GraphTextVisibilityManager`: Main graph text management
- `PlotlyTextEnhancer`: Specifically handles Plotly chart text visibility
- `ContrastAnalyzer`: Analyzes and fixes text/background contrast issues

**Interface**:
```python
class GraphTextVisibilityManager:
    def enhance_plotly_text_visibility(self) -> None
    def fix_dashboard_graph_contrast(self) -> None
    def apply_chart_text_styles(self, chart_config: dict) -> dict
    def ensure_readable_labels(self) -> None
```

### 4. Print Media Controller

**Purpose**: Remove unwanted print features and manage print-specific styling

**Key Components**:
- `PrintMediaController`: Manages print media queries and features
- `PrintFeatureRemover`: Removes unwanted print UI elements
- `PrintStyleManager`: Manages print-specific CSS

**Interface**:
```python
class PrintMediaController:
    def remove_print_features(self) -> None
    def apply_print_media_queries(self) -> None
    def hide_print_controls(self) -> None
    def optimize_print_layout(self) -> None
```

## Data Models

### ContentFilterConfig
```python
@dataclass
class ContentFilterConfig:
    filter_ingredient_html: bool = True
    sanitize_display_content: bool = True
    remove_raw_tags: bool = True
    preserve_formatting: bool = True
```

### IconConfig
```python
@dataclass
class IconConfig:
    icon_font_url: str = "https://fonts.googleapis.com/icon?family=Material+Icons"
    fallback_icons: Dict[str, str]
    sidebar_icon_mappings: Dict[str, str]
```

### GraphTextConfig
```python
@dataclass
class GraphTextConfig:
    min_contrast_ratio: float = 4.5
    default_text_color: str = "#000000"
    background_color: str = "#ffffff"
    font_weight: str = "600"
    font_size: int = 14
```

## Error Handling

### HTML Content Filtering Errors
- **Malformed HTML**: Gracefully handle and sanitize malformed HTML content
- **Missing Content**: Provide fallback content when filtering removes all content
- **Performance Issues**: Implement caching for frequently filtered content

### Icon Rendering Errors
- **Missing Icons**: Provide text fallbacks when icons fail to load
- **Font Loading Failures**: Implement retry mechanisms and alternative icon sources
- **Browser Compatibility**: Ensure icons work across different browsers

### Graph Text Visibility Errors
- **Contrast Calculation Failures**: Use safe default colors when contrast analysis fails
- **Chart Rendering Issues**: Provide fallback styling for unsupported chart types
- **Dynamic Content**: Handle dynamically generated chart content

### Print Media Errors
- **CSS Override Conflicts**: Ensure print styles don't interfere with screen display
- **Feature Detection**: Gracefully handle browsers that don't support certain print features

## Testing Strategy

### Unit Tests
- Test HTML content filtering with various input scenarios
- Verify icon replacement functionality with different text patterns
- Test graph text contrast calculations with various color combinations
- Validate print media query application

### Integration Tests
- Test complete UI rendering pipeline with filtered content
- Verify icon display across different browser environments
- Test graph readability in various dashboard configurations
- Validate print functionality without unwanted features

### Visual Regression Tests
- Compare before/after screenshots of ingredient lists
- Verify sidebar icons display correctly
- Test dashboard graph text visibility
- Ensure print layouts are clean and functional

### Accessibility Tests
- Verify text contrast meets WCAG guidelines
- Test screen reader compatibility with filtered content
- Validate keyboard navigation with icon elements
- Ensure print versions are accessible

## Performance Considerations

### HTML Content Filtering
- Implement efficient regex patterns for HTML tag detection
- Cache filtered content to avoid repeated processing
- Use streaming processing for large content blocks

### Icon Rendering
- Lazy load icon fonts to improve initial page load
- Implement icon sprite sheets for better performance
- Cache icon mappings in browser storage

### Graph Text Visibility
- Pre-calculate optimal text colors for common backgrounds
- Use CSS custom properties for dynamic color updates
- Minimize DOM manipulation during chart updates

### Print Media Management
- Use CSS-only solutions where possible to avoid JavaScript overhead
- Implement efficient media query detection
- Minimize print-specific CSS to reduce bundle size

## Security Considerations

### HTML Content Sanitization
- Prevent XSS attacks through proper HTML sanitization
- Validate all user-generated content before processing
- Use allowlist approach for permitted HTML elements

### Icon Loading
- Validate icon font sources to prevent malicious content
- Implement Content Security Policy for external font loading
- Use integrity checks for external icon resources

### Graph Data Security
- Sanitize chart data to prevent code injection
- Validate color values to prevent CSS injection
- Ensure chart configurations don't expose sensitive data

## Implementation Phases

### Phase 1: HTML Content Filtering (Priority: Critical)
1. Implement `CriticalHTMLContentFilter` class
2. Create Streamlit content interceptors
3. Add ingredient list processing
4. Test with existing meal planning content

### Phase 2: Icon Rendering Fixes (Priority: High)
1. Implement `IconRenderingManager` class
2. Load Material Design icon fonts
3. Create sidebar icon mappings
4. Test icon display across browsers

### Phase 3: Graph Text Visibility (Priority: High)
1. Implement `GraphTextVisibilityManager` class
2. Enhance Plotly chart text visibility
3. Add contrast analysis and fixes
4. Test with dashboard graphs

### Phase 4: Print Media Management (Priority: Medium)
1. Implement `PrintMediaController` class
2. Remove unwanted print features
3. Optimize print layouts
4. Test print functionality

### Phase 5: Integration and Testing (Priority: High)
1. Integrate all components into main application
2. Conduct comprehensive testing
3. Performance optimization
4. Documentation and deployment