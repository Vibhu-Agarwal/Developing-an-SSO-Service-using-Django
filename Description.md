# Developing a Single-Sign-On service using Django

Single-Sign-On (SSO) allows users to authenticate with a single ID and password to any of several related, yet independent, software systems. Google's authentication system is one such example through which it allows users to sign-in to YouTube, G-Mail, Docs and several other other products.

We'll be discussing how a SSO works and how it can be designed, architected and implemented in Python using Django (REST Framework). This will also feature the particular implementation, being used at [Viga Studios](https://vigastudios.com/) to develop a SSO service for all of their products.

## How SSO works
The SSO is developed to provide a single-point for managing authorization and authentication for individual services which can be on any platform: Mobile, Desktop or Web. The SSO service handles all the authorization part and *most* of the authentication part is carried out by individual services based on the particular service's use-case.  
Users are redirected to SSO when requested for resources which need authentication. Authentication is then handled by the SSO following some protocol (most common ones listed below).  
Sessions store the data for making further authorized requests and can be maintained at different points: SSO-level, Local Session or Identity Provider Session.

### Different Protocols

 - [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)
 - [Lightweight Directory Access Protocol](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol)
 - [OpenID Connect](https://openid.net/connect/)

### OpenID Connect (OIDC)

> OIDC is an authentication protocol, based on the OAuth 2.0 family of
> specifications. It uses simple JSON Web Tokens (JWT), which can be
> obtained using flows conforming to the [OAuth 2.0 specifications](https://www.oauth.com/oauth2-servers/map-oauth-2-0-specs/).

We'll be following OIDC and using [JWT](https://jwt.io/) for transferring [Access Tokens](https://tools.ietf.org/html/rfc6749#section-1.4) and [Refresh Tokens](https://tools.ietf.org/html/rfc6749#section-1.5) through HTTP(s).

## Using Django to develop a SSO service
We will walk through each of these sections discussing the implementation, what was the need and **why** a particular method was adopted.

### Access Tokens
 - Using [JWT](https://jwt.io/) with [DRF](https://www.django-rest-framework.org/)
 - Access and Refresh Tokens
 - Customizing Token Claims

### Asymmetric Keys
 - Need of using asymmetric keys
 - Using [cryptography](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/) for generating asymmetric keys

### Designing Database

 - Key [models](https://docs.djangoproject.com/en/3.0/topics/db/models/) needed to set-up the service

### Using Business-Specific Permissions and developing APIs
 - Writing [Custom Permssions](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions)
 - Quickly develop APIs using DRF's [Generic-API-Views](https://www.django-rest-framework.org/api-guide/generic-views/)

### Integrating Services
 - Configuring SSO to integrate individual (separate) services

