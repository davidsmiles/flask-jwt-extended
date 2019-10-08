# A RESTful API

Implemented using Flask-RESTFul, Flask-JWT_Extended and Flask-SQLAlchemy.


#### _Milestone_
1. Blacklisting user's token on logging out `@app.token_in_blacklist_loader`
2. Requiring fresh token `@app.fresh_jwt_required`
3. Refreshing user's token  `@jwt_refresh_token_required`
4. Customizing JWT method callbacks including
`@app.expired_token_loader`
`@app.invalid_token_loader`
`@app.unauthorized_loader`
`@app.need_fresh_token_loader`
`@app.revoked_token_loader`
`@app.`
5. Making some endpoints have `@jwt_optional` and thereby return a half detail of the resource they requested.
6. Add claims `@jwt.user_claims_loader`, essentially this are extra piece of information we attach to the user's token when they send us a request
7. Getting the unique identifier `get_raw_jti()` of the user's token.

`