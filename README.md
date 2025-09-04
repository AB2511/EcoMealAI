# 🌱 EcoMealAI - Sustainable Meal Planning & Gamification

EcoMealAI is an intelligent meal planning application that helps users create sustainable, low-carbon weekly meal plans while gamifying their environmental impact reduction journey through achievements, streaks, and progress tracking.

## Features

### 📅 Weekly Meal Plan Generator
- **Automated Weekly Planning**: Generate complete 7-day meal plans with breakfast, lunch, and dinner
- **Smart Optimization**: Ingredient overlap optimization to minimize food waste and shopping complexity
- **Flexible Customization**: Drag-and-drop meal rearrangement and individual meal replacement
- **Constraint Satisfaction**: Respects dietary restrictions, budget limits, and carbon footprint goals

### 🎮 Carbon Footprint Gamification Dashboard
- **Achievement System**: Earn badges and points for carbon reduction milestones
- **Streak Tracking**: Maintain and celebrate consistent low-carbon eating habits
- **Progress Visualization**: Interactive charts showing daily, weekly, and monthly carbon trends
- **Goal Setting**: Set custom carbon reduction targets and track progress toward them

### 🛒 Shopping & Meal Prep Integration
- **Automated Shopping Lists**: Generate consolidated shopping lists with quantities and categories
- **Meal Prep Scheduling**: Optimal preparation order and batch cooking suggestions
- **Cost Tracking**: Track actual costs vs. estimates with item check-off functionality
- **Seasonal Highlighting**: Identify seasonal and local ingredient options

### 🤝 Social & Community Features
- **Achievement Sharing**: Share accomplishments with carbon savings statistics
- **Community Leaderboards**: Optional friendly competition with other users
- **Privacy Controls**: Full control over what information is shared publicly
- **Meal Plan Sharing**: Share successful sustainable meal plans with the community

### 🤖 Enhanced AI Recommendations
- **Machine Learning**: Advanced recipe suggestions using scikit-learn
- **Recipe Complementarity**: Nutritional and ingredient synergy analysis
- **Learning System**: Improves recommendations based on meal ratings and preferences
- **Variety Optimization**: Ensures diverse recipes across weekly meal plans

## Installation

### Option 1: Automated Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd EcoMealAI
   ```

2. **Run the appropriate setup script**:
   
   **Windows:**
   ```cmd
   install.bat
   ```
   
   **macOS/Linux:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   
   **Cross-platform (Python):**
   ```bash
   python setup.py
   ```
   
   These scripts will automatically install all dependencies and guide you through Tesseract OCR installation.

### Option 2: Manual Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd EcoMealAI
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the project root directory:
   ```bash
   # Create .env file
   touch .env
   ```
   
   Add your API keys to the `.env` file:
   ```env
   # Required: Climatiq API Key for enhanced carbon footprint calculations
   CLIMATIQ_API_KEY=your_climatiq_api_key_here
   
   # Optional: TheMealDB API Key (free tier doesn't require key)
   THEMEALDB_API_KEY=your_themealdb_api_key_here
   ```
   
   **Getting API Keys:**
   - **Climatiq API**: Sign up at [climatiq.io](https://www.climatiq.io/) for carbon footprint data
   - **TheMealDB API**: Free tier available at [themealdb.com](https://www.themealdb.com/api.php)

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

### Installation Verification

**Verify your installation is complete:**

1. **Check Python packages**:
   ```python
   import streamlit, pandas, numpy, sklearn, requests, plotly
   print("✅ All packages installed successfully")
   ```

2. **Test EcoMealAI features**:
   - Run the app: `streamlit run app.py`
   - Generate a weekly meal plan using the sidebar controls
   - Check the gamification dashboard for progress tracking
   - Verify shopping list generation works correctly

### Quick Start Guide

**Test the core features:**

1. **Weekly Meal Plan Generation**:
   - Set your dietary preferences in the sidebar
   - Configure carbon footprint and budget goals
   - Click "Generate Weekly Meal Plan"
   - Review the 7-day meal plan with sustainability metrics

2. **Gamification Dashboard**:
   - Check your carbon footprint progress charts
   - View earned achievements and badges
   - Monitor your streak counters
   - Set and track carbon reduction goals

3. **Shopping List Generation**:
   - Generate a meal plan first
   - Click "Generate Shopping List"
   - Review categorized ingredients with quantities
   - Check off items and track costs

**Successful test indicators:**
- ✅ Weekly meal plan generates with 21 meals (7 days × 3 meals)
- ✅ Carbon footprint calculations display for each meal
- ✅ Achievement system awards points for low-carbon choices
- ✅ Shopping list consolidates ingredients across all meals
- ✅ Progress charts show carbon footprint trends

## Testing the Meal Planning Features

### Weekly Meal Plan Generator Testing

**Test different dietary preferences:**
- **Vegetarian**: Should generate plant-based meals with appropriate protein sources
- **Vegan**: Should exclude all animal products including dairy and eggs
- **Gluten-Free**: Should avoid wheat, barley, rye, and other gluten-containing ingredients
- **Low-Carbon**: Should prioritize recipes with minimal environmental impact

**Test constraint satisfaction:**
- **Budget Limits**: Set a low budget ($5/serving) and verify all meals stay within limit
- **Carbon Goals**: Set strict carbon limits (2kg CO2/serving) and check compliance
- **Prep Time**: Set short prep times (30 minutes) and verify meal complexity

### Gamification System Testing

**Achievement System:**
- Generate low-carbon meal plans to earn "Eco Warrior" badges
- Maintain consistent carbon reduction to build streaks
- Try diverse recipes to unlock "Recipe Explorer" achievements

**Progress Tracking:**
- Generate multiple meal plans to see carbon footprint trends
- Set carbon reduction goals and monitor progress
- Check that charts update with new meal plan data

**Expected Results:**
- Points awarded based on carbon footprint reduction
- Badges unlocked when thresholds are met
- Streak counters increment with consistent low-carbon choices
- Progress charts show improvement trends over time

### Environment Variables Setup

The application uses environment variables for secure API key management. Here's how to set them up:

#### Option 1: Using .env file (Recommended)
Create a `.env` file in your project root:
```env
CLIMATIQ_API_KEY=your_actual_climatiq_api_key
THEMEALDB_API_KEY=your_themealdb_api_key  # Optional
```

#### Option 2: System Environment Variables
Set environment variables in your system:

**Windows:**
```cmd
set CLIMATIQ_API_KEY=your_actual_climatiq_api_key
```

**macOS/Linux:**
```bash
export CLIMATIQ_API_KEY=your_actual_climatiq_api_key
```

#### Option 3: Streamlit Secrets (for deployment)
For Streamlit Cloud deployment, add secrets in your Streamlit dashboard:
```toml
# .streamlit/secrets.toml
CLIMATIQ_API_KEY = "your_actual_climatiq_api_key"
THEMEALDB_API_KEY = "your_themealdb_api_key"
```

### Security Notes

- **Never commit API keys** to version control
- The `.env` file is included in `.gitignore` to prevent accidental commits
- Use different API keys for development and production environments
- Regularly rotate your API keys for security

## Troubleshooting

### Common Issues

**"Missing Environment Variables" Error:**
- Ensure your `.env` file exists in the project root directory
- Check that your `.env` file contains the required API keys
- Verify there are no extra spaces around the `=` sign in your `.env` file
- Restart the application after creating/modifying the `.env` file

**API Connection Issues:**
- Verify your API keys are valid and active
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**Recipe Loading Problems:**
- The app will fall back to sample recipes if the API is unavailable
- Check the console for detailed error messages
- Try adjusting your dietary preferences if no recipes are found

### Meal Planning Troubleshooting

#### Meal Plan Generation Issues

**"No recipes found" error:**
- ✅ **Try**: Relax dietary restrictions or budget constraints
- ✅ **Try**: Increase carbon footprint limit or preparation time
- ✅ **Check**: Ensure API keys are properly configured
- ✅ **Fallback**: App will use sample recipes if API is unavailable

**"Optimization failed" message:**
- ✅ **Try**: Reduce the number of constraints (budget, carbon, time)
- ✅ **Try**: Allow more variety in cuisine types
- ✅ **Check**: Ensure sufficient recipes are available for your preferences

#### Gamification System Issues

**Points not calculating correctly:**
- ✅ **Check**: Ensure meal plans are being generated successfully
- ✅ **Verify**: Carbon footprint calculations are working
- ✅ **Try**: Refresh the dashboard to update progress

**Achievements not unlocking:**
- ✅ **Check**: Review achievement thresholds in the dashboard
- ✅ **Try**: Generate more meal plans to accumulate progress
- ✅ **Verify**: Carbon reduction is meeting badge requirements

#### Shopping List Issues

**Missing ingredients:**
- ✅ **Check**: Ensure meal plan was generated successfully first
- ✅ **Try**: Regenerate the meal plan and shopping list
- ✅ **Verify**: All meals in the plan have ingredient data

**Incorrect quantities:**
- ✅ **Check**: Recipe serving sizes and scaling factors
- ✅ **Try**: Adjust serving preferences in meal plan settings
- ✅ **Report**: Note any consistently incorrect calculations

### Getting Help

If you encounter issues:
1. Check the console output for detailed error messages
2. Verify your `.env` file setup using the provided `.env.example`
3. Ensure all dependencies are installed correctly
4. Try running with sample data first to verify the app works

## Usage

### Setting Up Your Profile

1. **Dietary Preferences**: Select from vegetarian, vegan, gluten-free, low-carb, high-protein, and omega-3 options
2. **Budget Constraint**: Set your maximum cost per serving ($1-$20)
3. **Carbon Footprint Goal**: Choose your target carbon footprint reduction (10-50%)
4. **Preparation Time**: Set maximum cooking time (10-120 minutes)
5. **Cuisine Preferences**: Select preferred cuisine types for variety

### Generating Weekly Meal Plans

#### Basic Meal Plan Generation:
1. **Configure preferences** in the sidebar controls
2. **Set weekly goals** for carbon footprint and budget
3. **Click "Generate Weekly Meal Plan"** to create a complete 7-day plan
4. **Review the plan** with sustainability metrics and cost breakdown

#### Customizing Your Meal Plan:
1. **Drag and drop meals** to rearrange within the weekly view
2. **Replace individual meals** while maintaining weekly goals
3. **Adjust serving sizes** to match your household needs
4. **Save meal plan templates** for future reuse

#### Advanced Features:
- **Ingredient optimization**: Minimizes shopping complexity through ingredient reuse
- **Nutritional balance**: Ensures balanced nutrition across the week
- **Variety enforcement**: Prevents recipe repeats within the same week
- **Constraint satisfaction**: Respects all dietary, budget, and carbon goals

### Using the Gamification Dashboard

#### Tracking Progress:
1. **View carbon footprint trends** in interactive charts
2. **Monitor achievement progress** toward badges and milestones
3. **Track streak counters** for consistent low-carbon eating
4. **Set custom goals** and monitor progress toward them

#### Earning Achievements:
- **Eco Warrior**: Achieve >50% carbon reduction from baseline
- **Green Champion**: Achieve >30% carbon reduction
- **Recipe Explorer**: Try 10+ different low-carbon recipes
- **Streak Master**: Maintain 7-day low-carbon streak

### Managing Shopping and Meal Prep

#### Shopping List Generation:
1. **Generate a meal plan** first to populate ingredients
2. **Click "Generate Shopping List"** for consolidated ingredients
3. **Review categorized items** grouped by store section
4. **Check off items** and track actual costs vs. estimates

#### Meal Prep Planning:
1. **View prep schedule** with optimal preparation order
2. **Identify batch cooking opportunities** across recipes
3. **Follow storage recommendations** for prepared meals
4. **Use reheating instructions** for meal prep efficiency

### Understanding Sustainability Metrics

- **🟢 Low Carbon (< 3 kg CO2)**: Plant-based meals with minimal processing
- **🟡 Medium Carbon (3-5 kg CO2)**: Meals with some animal products
- **🔴 High Carbon (> 5 kg CO2)**: Meat-heavy or highly processed meals

## Technical Architecture

### Core Components

1. **WeeklyMealPlanGenerator**: Generates optimized 7-day meal plans with constraint satisfaction
2. **GamificationDashboard**: Tracks progress, calculates points, and manages achievement system
3. **MealPlanOptimizer**: Optimizes ingredient overlap and minimizes food waste
4. **CarbonFootprintTracker**: Records and analyzes historical carbon footprint data
5. **AchievementSystem**: Manages badges, streaks, and milestone detection
6. **EnhancedMealRecommendationEngine**: ML-powered recommendation system with weekly planning logic

### Machine Learning Features

- **Weekly Planning Logic**: Considers recipe variety and nutritional balance across 7 days
- **Ingredient Complementarity**: Analyzes nutritional and ingredient synergy between recipes
- **Learning System**: Improves recommendations based on meal ratings and user feedback
- **Multi-criteria Optimization**: Balances carbon footprint, cost, nutrition, and variety
- **Constraint Satisfaction**: Ensures all dietary restrictions and goals are met

### Gamification System

- **Point Calculation**: Awards points based on carbon footprint reduction achieved
- **Achievement Triggers**: Detects milestone completion and awards appropriate badges
- **Streak Tracking**: Monitors consistent low-carbon eating habits
- **Progress Analytics**: Provides insights and personalized improvement recommendations

## Data Sources

### Carbon Footprint Data
The application includes comprehensive carbon footprint data for common ingredients:
- **Proteins**: Beef (27.0 kg CO2/kg), Chicken (6.1 kg CO2/kg), Tofu (2.0 kg CO2/kg)
- **Dairy**: Cheese (13.5 kg CO2/kg), Milk (3.2 kg CO2/kg)
- **Grains**: Rice (2.7 kg CO2/kg), Quinoa (1.8 kg CO2/kg)
- **Vegetables**: Most vegetables (0.3-1.1 kg CO2/kg)

### Recipe Database
Sample recipes include:
- Lentil Buddha Bowl (Low carbon, vegetarian)
- Grilled Chicken Salad (Medium carbon, high protein)
- Vegetable Stir Fry (Low carbon, vegan)
- Quinoa Stuffed Bell Peppers (Low carbon, vegetarian)
- Salmon with Roasted Vegetables (Medium carbon, omega-3)

## Customization

### Adding New Recipes
Edit the `RecipeDatabase._initialize_recipes()` method in `app.py` to add new recipes with the following structure:

```python
{
    'name': 'Recipe Name',
    'ingredients': {'ingredient1': amount_in_kg, 'ingredient2': amount_in_kg},
    'prep_time': minutes,
    'servings': number,
    'difficulty': 'Easy/Medium/Hard',
    'cuisine': 'Cuisine Type',
    'dietary_tags': ['tag1', 'tag2'],
    'cost_per_serving': cost_in_usd,
    'instructions': 'Cooking instructions'
}
```

### Updating Carbon Footprint Data
Modify the `carbon_data` dictionary in `CarbonFootprintCalculator.__init__()` to add or update ingredient carbon footprints.

### Extending ML Features
The recommendation engine can be enhanced by:
- Adding more sophisticated feature engineering
- Implementing collaborative filtering
- Including user rating systems
- Adding seasonal ingredient preferences

## Future Enhancements

- **🔌 Enhanced API Integration**: Connect to more recipe and nutrition databases
- **📱 Mobile App**: Native mobile application for meal planning on-the-go
- **🤝 Social Features Expansion**: Recipe sharing, community challenges, and group meal planning
- **🧠 Advanced AI**: More sophisticated meal recommendation algorithms and personalization
- **🌍 Localization**: Support for regional ingredients, cuisines, and carbon footprint data
- **📊 Advanced Analytics**: Deeper insights into eating patterns and sustainability trends
- **🏆 Expanded Gamification**: More achievement types, seasonal challenges, and reward systems
- **🔗 Third-party Integrations**: Grocery delivery services, fitness trackers, and smart kitchen devices

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Carbon footprint data sourced from environmental research studies
- Built with Streamlit, scikit-learn, and Plotly
- Inspired by the need for sustainable food choices in climate action

---

**Made with 🌱 for a sustainable future**