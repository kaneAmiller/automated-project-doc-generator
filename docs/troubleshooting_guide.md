# Troubleshooting Guide

## Common API Errors

### Invalid Token
**Description**: This error occurs when the provided API token is invalid or has been revoked.  
**Solution**: Ensure that you are using a valid API token. You can generate a new token from the Asana Developer Console and replace it in your configuration.

### Workspace or Project Not Found
**Description**: This error indicates that the specified workspace or project ID does not exist or is not accessible.  
**Solution**: Verify that you are using the correct workspace ID and project ID. Ensure that the project exists in your Asana account and that your API token has permission to access it.

### Rate Limit Exceeded
**Description**: Asana imposes rate limits on API requests. Exceeding this limit results in an error.  
**Solution**: Reduce the frequency of your API requests and try again later. Monitor your request count and spread requests over a longer period.

## Common Template Rendering Issues

### Missing Placeholders
**Description**: If the rendered document is missing certain sections, it may be due to missing data or incorrect placeholders in the templates.  
**Solution**: Ensure that the data being passed to the template includes all expected keys. Verify that placeholders in the template match the keys in your data dictionary.

### Incorrect Template Format
**Description**: The output format may not display as expected if the template contains syntax errors.  
**Solution**: Review the template syntax for Jinja2. Ensure that all variables are correctly referenced and that there are no typos.

## Export Errors

### Missing Dependencies
**Description**: Errors related to PDF export may occur if the required dependencies (like `wkhtmltopdf`) are not installed.  
**Solution**: Make sure to install `wkhtmltopdf` on your system. You can use Homebrew on macOS to install it:
```bash
brew install wkhtmltopdf
```

### File Not Found
**Description**: This error indicates that the specified HTML file for conversion does not exist.  
**Solution**: Verify that the HTML file is being correctly generated and saved before attempting to convert it to PDF. Check the output directory path.
