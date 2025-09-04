# Design Document

## Overview

This design addresses critical UI issues in the EcoMealAI application by implementing targeted fixes for recipe image display, nutritional information, shopping list formatting, export functionality, achievement display, accessibility features, keyboard shortcuts, and visual consistency.

## Architecture

### Component Structure
```
UI Critical Fixes
├── Image Display Manager
│   ├── Recipe Image Handler
│   └── Placeholder Image System
├── Content Formatting System
│   ├── HTML Tag Sanitizer
│   ├── Text Formatter
│   └── Layout Optimizer
├── Keyboard Shortcut Manager
│   ├── Event Listener System
│   └── Action Dispatcher
├── Accessibility Enhancement Manager
│   ├── Skip Link Handler
│   └── Focus Management
└── Visual Consistency Manager
    ├── CSS Style Injector
    └── Theme Consistency Checker
```

## Components and Interfaces

### 1. Image Display Manager

**Purpose**: Ensure recipe images are properly displayed with fallbacks

**Key Methods**:
- `display_recipe_image(recipe_data, container_width=True)`
- `get_placeholder_image(recipe_type)`
- `validate_image_url(url)`

**Implementation Strategy**:
- Use `st.image()` with `use_container_width=True` (not deprecated parameter)
- Implement try-catch for image loading failures
- Provide themed placeholder images for missing recipes
- Add image lazy loading for performance

### 2. Content Formatting System

**Purpose**: Clean up HTML tags and improve text display

**Key Methods**:
- `sanitize_html_content(content)`
- `format_shopping_item_display(item)`
- `clean_recipe_source_text(source_text)`

**Implementation Strategy**:
- Use `html.unescape()` and regex to remove HTML tags
- Create consistent formatting templates for shopping items
- Implement proper text wrapping and spacing

### 3. Nutritional Information Handler

**Purpose**: Display meaningful nutritional data or appropriate loading states

**Key Methods**:
- `get_nutritional_summary(meal_plan)`
- `display_nutrition_loading_state()`
- `format_nutrition_display(nutrition_data)`

**Implementation Strategy**:
- Implement actual nutritional calculation logic
- Add loading spinners during calculation
- Provide detailed breakdown of macronutrients and micronutrients
- Handle missing data gracefully with informative messages

### 4. Keyboard Shortcut Manager

**Purpose**: Implement functional keyboard shortcuts for navigation and actions

**Key Methods**:
- `register_keyboard_shortcuts()`
- `handle_shortcut_event(key_combination)`
- `execute_shortcut_action(action)`

**Implementation Strategy**:
- Use Streamlit's `st.components.v1.html()` to inject JavaScript event listeners
- Map keyboard combinations to specific application actions
- Implement proper event handling and prevention of default browser behavior
- Add visual feedback for shortcut activation

### 5. Export Preview Manager

**Purpose**: Fix export preview positioning and sizing

**Key Methods**:
- `show_export_preview(shopping_list_data)`
- `format_export_content(data)`
- `handle_export_modal()`

**Implementation Strategy**:
- Use `st.modal()` or `st.expander()` for proper preview display
- Implement responsive sizing for different screen sizes
- Add proper close functionality and state management

### 6. Achievement Display System

**Purpose**: Improve achievement visibility and formatting

**Key Methods**:
- `display_achievements(achievements_data)`
- `format_achievement_card(achievement)`
- `apply_achievement_styling()`

**Implementation Strategy**:
- Use proper CSS styling for achievement cards
- Implement high contrast colors for better visibility
- Add proper spacing and typography hierarchy
- Include achievement icons and progress indicators

### 7. Accessibility Enhancement Manager

**Purpose**: Fix skip links and improve accessibility navigation

**Key Methods**:
- `render_skip_links()`
- `apply_accessibility_styles()`
- `manage_focus_states()`

**Implementation Strategy**:
- Implement proper skip link styling with focus states
- Add ARIA labels and roles where needed
- Ensure proper tab order and keyboard navigation
- Use semantic HTML structure

## Data Models

### Recipe Image Data
```python
@dataclass
class RecipeImageData:
    url: Optional[str]
    alt_text: str
    placeholder_type: str
    loading_state: bool
```

### Nutritional Summary Data
```python
@dataclass
class NutritionalSummary:
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: float
    vitamins: Dict[str, float]
    minerals: Dict[str, float]
    calculation_status: str
```

### Keyboard Shortcut Configuration
```python
@dataclass
class KeyboardShortcut:
    key_combination: str
    action: str
    description: str
    enabled: bool
```

## Error Handling

### Image Loading Errors
- Graceful fallback to placeholder images
- Log image loading failures for debugging
- Retry mechanism for temporary network issues

### Nutritional Calculation Errors
- Display informative error messages instead of generic placeholders
- Provide partial nutritional data when available
- Implement fallback calculations using ingredient databases

### Keyboard Shortcut Conflicts
- Detect and resolve conflicts with browser shortcuts
- Provide alternative key combinations when needed
- Allow users to customize shortcuts

## Testing Strategy

### Unit Tests
- Test image display with various input scenarios
- Test HTML sanitization with different content types
- Test keyboard shortcut registration and execution
- Test nutritional calculation accuracy

### Integration Tests
- Test complete user workflows with fixes applied
- Test accessibility compliance with screen readers
- Test responsive design across different screen sizes
- Test keyboard navigation flow

### Visual Regression Tests
- Compare before/after screenshots of fixed components
- Test achievement display consistency
- Test export preview functionality
- Test skip link visibility and styling

## Implementation Approach

### Phase 1: Content Display Fixes
1. Fix recipe image display issues
2. Implement HTML tag sanitization
3. Fix nutritional information display
4. Improve shopping list item formatting

### Phase 2: Interactive Features
1. Implement functional keyboard shortcuts
2. Fix export preview positioning
3. Enhance achievement display
4. Improve accessibility features

### Phase 3: Visual Polish
1. Apply consistent styling across components
2. Improve text contrast and readability
3. Optimize responsive design
4. Add loading states and transitions

## CSS Styling Strategy

### Custom CSS Injection
```css
/* Skip links styling */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    z-index: 1000;
}

.skip-link:focus {
    top: 6px;
}

/* Achievement styling */
.achievement-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}

/* High contrast mode */
.high-contrast .achievement-card {
    background: #000;
    border: 2px solid #fff;
    color: #fff;
}
```

### Responsive Design Considerations
- Mobile-first approach for all components
- Flexible grid layouts for different screen sizes
- Touch-friendly interactive elements
- Proper text scaling for accessibility

## Performance Considerations

### Image Optimization
- Lazy loading for recipe images
- Image compression and caching
- Progressive loading for large images

### JavaScript Optimization
- Minimal JavaScript injection for keyboard shortcuts
- Event delegation for better performance
- Debounced event handlers to prevent excessive calls

### CSS Optimization
- Minimal CSS injection to avoid conflicts
- Use of CSS custom properties for theming
- Efficient selectors to minimize rendering impact