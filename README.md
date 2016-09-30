# flask-csp

Add a Content Security Policy header to your Flask application.
More information on CSP:
* [w3c documentation](http://www.w3.org/TR/CSP2/)
* [useful guide](http://www.html5rocks.com/en/tutorials/security/content-security-policy/)

## Installation

Since this is a fork, you have to install manually. Clone the repo and run

```bash
$ python setup.py install
```

## Usage
Add the csp_header(...) decorator after the app.route(...) decorator to create a csp header on each route. The decorator can either be passed no value (Add default policies) or custom values by a dict (Add custom policies). For more information on the default policies see "Change Default Policies" below.

### Add default header
```python
from flask_csp.csp import FlaskCSP
csp = FlaskCSP()

@app.route('/')
@csp.csp_header()
```

### Set defaults once

```python
from flask_csp.csp import FlaskCSP
csp = FlaskCSP({
    "script-src": "'self'"
})

@app.route('/')
@csp.csp_header()
```

All the decorators will now use the defaults given to `FlaskCSP`. You can
override this per route as seen below.

### Custom header per route
Pass the csp_header wrapper a dict with the policies to change:
```python
@app.route('/')
@csp.csp_header({'default-src':"'none'",'script-src':"'self'"})
```
Notes: 
* Only policies with a non empty value are added to the header. The wrapper @csp_header({'default-src':""}) will remove 'default-src ...' from the header
* 4 keywords in policies must always be encapsulated in single quotes: 'none', 'self', 'unsafe-inline','unsafe-eval'
* The data permission is spelled with a colon
  * ex: @csp_header({'default-src':"'none'",'script-src':"'self'", 'font-src': "data: 'self'"})

### Report only header
To set the header to "Report only" pass the key/value pair 'report-only':True to the custom header dict:
```python
from flask_csp.csp import FlaskCSP
csp = FlaskCSP()

@app.route('/')
@csp.csp_header({'report-only':True})
```

## Change Default Policies
The default policies are as follows:
```json
{
  "default-src": "'self'",
  "script-src": "",
  "img-src": "",
  "object-src": "",
  "plugin-src": "",
  "style-src": "",
  "media-src": "",
  "child-src": "",
  "connect-src": "",
  "base-uri": "",
  "report-uri": "/csp_report"
}
```
Edit default policies via command line:
```python
>>> from flask_csp.csp import FlaskCSP
>>> csp = FlaskCSP()
>>> csp.update_defaults({'child-src':"'self'"})
```
Edit default policies on flask app:
```python
from flask_csp.csp import FlaskCSP

csp = FlaskCSP()
csp.update_defaults({'script-src':"'self' code.jquery.com"})
```

To view the default policies:
```python
>>> from flask_csp.csp import FlaskCSP
>>> csp = FlaskCSP()
>>> csp.defaults
```
Note: 
* Python interpreter must be reloaded for changes to the default policies to take place

## Violation Reports
Based on the default settings, reports will be sent to the route 'csp_report' through a POST request. This is totally customizable but here is a very simplistic example of handling these reports:
```python
@app.route('/csp_report',methods=['POST'])
def csp_report():
    with open('/var/log/csp/csp_reports'), "a") as fh:
        fh.write(request.data+"\n")
    return 'done'
```
