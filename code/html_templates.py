__all__ = "OUTPUT_TEMPLATE"

OUTPUT_TEMPLATE = """
<form>
  <input type="radio" name="action" value="retrieve">Retrieve a Ressource</option>
  <input type="radio" name="action" value="history">Show history</option>
  <input type="submit" value="Run" />
</form>
<hr />

%s
"""
