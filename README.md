# A RESTful API

Implemented using Flask-RESTFul, Flask-JWT_Extended and Flask-SQLAlchemy.


#### _Milestone_
1. Blacklisting user's token on logging out `@jwt.token_in_blacklist_loader`
2. Requiring fresh token `@jwt.fresh_jwt_required`
3. Refreshing user's token  `@jwt_refresh_token_required`
4. Customizing JWT method callbacks including
`@jwt.expired_token_loader`
`@jwt.invalid_token_loader`
`@jwt.unauthorized_loader`
`@jwt.need_fresh_token_loader`
`@jwt.revoked_token_loader`
5. Making some endpoints have `@jwt_optional` and thereby return a half detail of the resource they requested.
6. Add claims `@jwt.user_claims_loader`, essentially this are extra piece of information we attach to the user's token when they send us a request
7. Passing the user object as identity in `create_access_token` and then it calls the `@jwt.user_identity_loader` to define what the identity of the access_token should be. 
8. Getting the unique identifier `get_raw_jti()` of the user's token.

`