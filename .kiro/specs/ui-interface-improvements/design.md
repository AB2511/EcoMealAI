# Design Document

## Overview

This design addresses critical UI/UX improvements for the meal planning application, focusing on fixing deprecated Streamlit parameters, enhancing recipe management capabilities, improving weekly plan generation reliability, and implementing proper interface separation. The solution maintains backward compatibility while modernizing the codebase and improving user experience through better navigation and feature isolation.

## Architecture

### Current Architecture Analysis

The application currently uses a single-page architecture with conditional rendering based on session state flags:
- `show_weekly_plan`: Controls weekly meal plan display
- `show_shopping_list`: Controls shopping list overlay
- Main content area switches between recommendation engine and meal planning views

### Proposed Architecture

**Multi-View Navigation System**
- Implement a proper navigation system with distinct views
- Use Streamlit's native navigation capabilities with clear state management
- Separate interfaces for: Meal Planning, Dashboard, Shopping List, Recipe Browser

**State Management Enhancement**
- Centralized session state management
- Persistent user preferences and saved recipes
- Clear state transitions between views

## Components and Interfaces

### 1. Navigation Component

**NavigationManager Class**
```python
class NavigationManager:
    def __init__(self):
        self.views = {
            'meal_planning': 'Weekly Meal Planning',
            'dashboard': 'Progress Dashboard', 
            'shopping': 'Shopping List',
            'recipes': 'Recipe Browser'
        }
    
    def render_navigation(self):
        # Sidebar navigation with clear view selection
        
    def switch_view(self, view_name):
        # Handle view transitions with state preservation
```

### 2. Enhanced Recipe Management

**RecipeManager Class**
```python
class RecipeManager:
    def __init__(self):
        self.saved_recipes = []
        self.recipe_collections = {}
    
    def save_recipe(self, recipe):
        # Save recipe to user collection
        
    def add_recipe_to_plan(self, recipe, day, meal_type):
        # Add recipe to specific meal plan slot
        
    def get_saved_recipes(self):
        # Retrieve user's saved recipes
```

**Recipe Card Component**
- Enhanced recipe display with action buttons
- Save/unsave functionality with visual feedback
- Add to plan with day/meal selection modal
- Improved image display using `use_container_width`

### 3. Improved Weekly Plan Generator

**Enhanced WeeklyPlanGenerator**
```python
class EnhancedWeeklyPlanGenerator:
    def __init__(self, recipe_db, carbon_calc):
        self.recipe_db = recipe_db
        self.carbon_calc = carbon_calc
        self.validation_rules = []
    
    def generate_plan_with_validation(self, preferences):
        # Generate plan with comprehensive validation
        
    def validate_plan(self, plan):
        # Validate dietary restrictions, carbon goals, etc.
        
    def handle_generation_errors(self, error):
        # Provide clear error messages and recovery options
```

### 4. Separate Interface Views

**View Components Structure**
```
├── MealPlanningView
│   ├── PlanGenerator (sidebar)
│   ├── WeeklyPlanDisplay (main)
│   └── QuickActions (buttons)
├── DashboardView  
│   ├── ProgressCharts
│   ├── Achievements
│   └── Analytics
├── ShoppingListView
│   ├── ItemList
│   ├── CategoryGroups
│   └── CostTracking
└── RecipeBrowserView
    ├── SearchFilters
    ├── RecipeGrid
    └── SavedRecipes
```

## Data Models

### Enhanced Session State Structure

```python
session_state = {
    # Navigation
    'current_view': 'meal_planning',
    'previous_view': None,
    
    # Recipe Management
    'saved_recipes': [],
    'recipe_collections': {},
    'current_recipe_filters': {},
    
    # Meal Planning
    'current_weekly_plan': None,
    'plan_generation_status': 'idle',
    'plan_validation_errors': [],
    
    # Interface States
    'show_recipe_modal': False,
    'selected_recipe_for_plan': None,
    'meal_slot_selection': {'day': None, 'meal': None},
    
    # User Preferences (persistent)
    'user_preferences': UserPreferences(),
    'ui_preferences': {
        'default_view': 'meal_planning',
        'sidebar_collapsed': False
    }
}
```

### Recipe Data Model Enhancement

```python
@dataclass
class EnhancedRecipe:
    # Existing fields
    id: str
    name: str
    ingredients: Dict[str, float]
    carbon_footprint: float
    
    # New fields for enhanced functionality
    is_saved: bool = False
    save_date: Optional[datetime] = None
    user_rating: Optional[int] = None
    custom_notes: str = ""
    usage_count: int = 0
```

## Error Handling

### Plan Generation Error Recovery

**Error Categories and Handling**
1. **No Recipes Found**: Suggest relaxing constraints or loading more recipes
2. **Constraint Conflicts**: Identify conflicting preferences and suggest adjustments
3. **API Failures**: Provide fallback recipes and retry mechanisms
4. **Validation Failures**: Clear messages about which requirements aren't met

**Error Display Strategy**
- Toast notifications for minor issues
- Modal dialogs for critical errors requiring user action
- Inline validation messages for form inputs
- Progress indicators for long-running operations

### User Input Validation

**Real-time Validation**
- Dietary preference compatibility checks
- Budget and carbon goal feasibility validation
- Ingredient availability verification
- Prep time constraint validation

## Testing Strategy

### Component Testing

**Unit Tests**
- NavigationManager view switching logic
- RecipeManager save/load operations
- Enhanced plan generation with various constraint combinations
- Error handling scenarios

**Integration Tests**
- View transitions with state preservation
- Recipe management across different views
- Plan generation with real recipe data
- Cross-component communication

### UI Testing

**Streamlit Component Tests**
- Image display with `use_container_width` parameter
- Navigation functionality across all views
- Recipe action buttons (save, add to plan)
- Modal dialogs and form interactions

**User Experience Tests**
- Interface separation verification
- State persistence across view changes
- Error message clarity and actionability
- Mobile responsiveness (where applicable)

### Performance Testing

**Load Testing**
- Large recipe database handling
- Multiple saved recipes management
- Complex meal plan generation
- View switching performance

## Implementation Approach

### Phase 1: Fix Deprecated Parameters
1. Replace `use_column_width` with `use_container_width`
2. Test image display consistency
3. Verify no deprecation warnings

### Phase 2: Implement Navigation System
1. Create NavigationManager class
2. Implement view switching logic
3. Add sidebar navigation
4. Test state preservation

### Phase 3: Enhanced Recipe Management
1. Create RecipeManager class
2. Implement save/unsave functionality
3. Add "Add to Plan" modal interface
4. Create saved recipes view

### Phase 4: Improve Plan Generation
1. Enhance error handling and validation
2. Add progress indicators
3. Implement retry mechanisms
4. Add plan customization options

### Phase 5: Separate Interface Views
1. Refactor existing components into separate views
2. Implement dedicated dashboard view
3. Create standalone shopping list view
4. Add recipe browser view

### Phase 6: Testing and Polish
1. Comprehensive testing of all components
2. User experience improvements
3. Performance optimization
4. Documentation updates

## Security Considerations

- Input validation for all user-provided data
- Safe handling of recipe data and user preferences
- Secure session state management
- Protection against malicious recipe content

## Accessibility Considerations

- Clear navigation labels and keyboard shortcuts
- Screen reader compatible interface elements
- High contrast mode support for charts and visualizations
- Responsive design for various screen sizes