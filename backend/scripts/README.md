# Scripts

Utility scripts for data analysis, model training, and maintenance.

---

## 📜 Available Scripts

### `analyze_irrigation_data.py`
Analyzes irrigation dataset and generates statistics.

**Purpose**: Data exploration and validation for smart irrigation model

**Usage**:
```bash
python scripts/analyze_irrigation_data.py
```

**Output**: Statistics, distributions, and insights about irrigation data

---

## 🔧 Adding New Scripts

When adding utility scripts:
1. Place in `scripts/` folder
2. Add descriptive docstring
3. Document usage here
4. Make executable with proper shebang if needed

### Script Categories
- **Data Analysis**: Scripts for exploring datasets
- **Model Training**: Scripts for training ML models (also in `app/modules/*/training_model/`)
- **Maintenance**: Scripts for database cleanup, migrations, etc.
- **Deployment**: Scripts for production deployment tasks

---

## 📝 Notes

### Script Location
- General utility scripts → `scripts/`
- Module-specific training → `app/modules/<module>/training_model/`
- Tests → `tests/`
- Documentation → `docs/`

### Best Practices
- Use argparse for command-line arguments
- Add logging for long-running scripts
- Include error handling
- Document dependencies in script docstring

---

**Last Updated**: 2024
