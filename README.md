# Horseradish

It burns, but not for long.

Horseradish is an image library for managing photographic assets and related metadata:

* various image sizes
* alt text and captions
* credit and source information
* notes and tags

## Settings

The following environment variables need to be configured on the instance.

### Google Auth

* GOOGLEAUTH_CLIENT_ID
* GOOGLEAUTH_CLIENT_SECRET
* GOOGLEAUTH_CALLBACK_DOMAIN
* GOOGLEAUTH_USE_HTTPS (default True)
* GOOGLEAUTH_APPS_DOMAIN (optional)
* GOOGLEAUTH_IS_STAFF (default False)

See [django-googleauth](https://github.com/jcarbaugh/django-googleauth) for more details.


### Amazon S3

* AWS_KEY
* AWS_SECRET
* AWS_BUCKET
* AWS_LOCATION (optional)


### Other

* DEBUG (default False)
* DATABASE_URL
* SECRET_KEY
* ELASTICSEARCH_URL
* ELASTICSEARCH_INDEX
* STATIC_ROOT
* RAVEN_DSN
