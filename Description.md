Single-Sign-On **(SSO)** allows users to authenticate with a single ID and password to any of several related, yet independent, software systems. Google's authentication system is one such example through which it allows users to sign-in to YouTube, G-Mail, Docs and several other products.

We'll be discussing how a SSO works and how it can be designed, architected and implemented in Python using Django (REST Framework). This will also feature the particular implementation, being used at [Viga Studios](https://vigastudios.com/) to develop a SSO service for all of their products.

### Who's this talk for?
 - Anyone who wants to know what goes on behind services like *'One-Account for all of Google'*
 - Anyone who's curious to know how a Single-Sign-On can be implemented for their own business
 - Anyone who wants to maintain a central database for storing their user data for a bunch of applications under them
 - Anyone who wants a way to separate their auth-server from their application-specific back-end
 - Anyone who wants to dive deep into authentication with Django

## How SSO works
- The SSO is developed to provide a single point for managing authorization and authentication for individual services which can be on any platform: Mobile, Desktop or Web. The SSO service handles all the authorization part and *most* of the authentication part is carried out by individual services based on the particular service's use-case.
- Users are redirected to SSO when requested for resources which need authentication. Authentication is then handled by the SSO following some protocol (most common ones listed below).
- Sessions store the data for making further authorized requests and can be maintained at different points: SSO-level, Local Session or Identity Provider Session.

#### Different Protocols

 - [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)
 - [Lightweight Directory Access Protocol](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol)
 - [OpenID Connect](https://openid.net/connect/)

#### OpenID Connect (OIDC)

> OIDC is an authentication protocol, based on the OAuth 2.0 family of
> specifications. It uses simple JSON Web Tokens (JWT), which can be
> obtained using flows conforming to the [OAuth 2.0 specifications](https://www.oauth.com/oauth2-servers/map-oauth-2-0-specs/).

 - **Access Tokens** are credentials used to access protected resources.  An access token is a string representing an authorization issued to the client.
 - **Refresh Tokens** are credentials used to obtain access tokens.

We'll be following OIDC and using [JSON Web Tokens (JWT)](https://jwt.io/) for transferring [Access Tokens](https://tools.ietf.org/html/rfc6749#section-1.4) and [Refresh Tokens](https://tools.ietf.org/html/rfc6749#section-1.5) through HTTP(s). We'll also have a short demo using [Postman](https://www.postman.com/) to see how to use JWT.


### Using Django to develop a SSO service
We will walk through each of these sections discussing the implementation, what was the need and **why** a particular method was adopted.

#### Outline

Discussion and a short demo on **Access and Refresh Tokens**

  - Using [JWT](https://jwt.io/) with [Django-Rest-Framework **(DRF)**](https://www.django-rest-framework.org/)
  - Customizing Token Claims (adding custom properties or key-value pairs in generated tokens)

Introduction to **Asymmetric Keys** and their usage

  - The need for using asymmetric algorithms for encryption
  - Using [cryptography](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/) for generating public and private keys
    - Private-keys can be used to decrypt messages which were encrypted with the *corresponding Public-key*, as well as to create signatures, which can be verified with the *corresponding Public-key*

**Designing Database**: Walk through the UML of the project

  - Key [models](https://docs.djangoproject.com/en/3.0/topics/db/models/) needed to set-up the service

**Using Business-Specific Permissions and developing APIs** (Code Walk-through)

  -  Writing [Custom Permssions](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions)
  - Quickly develop APIs using DRF's [Generic-API-Views](https://www.django-rest-framework.org/api-guide/generic-views/)

**Integrating Services**

 - Configuring SSO to integrate individual services
    - As the new services and products are created, their integration with SSO should require minimum effort and how we can configure the SSO to do that
