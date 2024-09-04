"""
Jacobson is a self hosted zipcode API
Copyright (C) 2023-2024 Christian G. Semke.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime
from typing import Annotated, Any, TypedDict

from typing_extensions import Doc


class JWTClaim(TypedDict, total=False):
	"""
	JSON Web Token (JWT) Claim.

	.. _iana: https://www.iana.org/assignments/jwt/jwt.xhtml
	"""

	sub: Annotated[Any, Doc('Subject.')]
	iss: Annotated[str, Doc('Issuer.')]
	aud: Annotated[str, Doc('Audience.')]
	exp: Annotated[datetime | int, Doc('Expiration Time.')]
	nbf: Annotated[datetime | int, Doc('Not Before.')]
	iat: Annotated[datetime | int, Doc('Issued At.')]
	jti: Annotated[str, Doc('JWT ID.')]
	name: Annotated[str, Doc('Full name.')]
	given_name: Annotated[str, Doc('Given name(s) or first name(s).')]
	family_name: Annotated[str, Doc('Surname(s) or last name(s).')]
	middle_name: Annotated[str, Doc('Middle name(s).')]
	nickname: Annotated[str, Doc('Casual name.')]
	preferred_username: Annotated[
		str,
		Doc('Shorthand name by which the End-User wishes to be referred to.'),
	]
	profile: Annotated[str, Doc('Profile page URL.')]
	picture: Annotated[str, Doc('Profile picture URL.')]
	website: Annotated[str, Doc('Web page or blog URL.')]
	email: Annotated[str, Doc('Preferred e-mail address.')]
	email_verified: Annotated[
		bool,
		Doc('True if the e-mail address has been verified; otherwise false.'),
	]
	gender: Annotated[str, Doc('Gender.')]
	birthdate: Annotated[str, Doc('Birthday.')]
	zoneinfo: Annotated[str, Doc('Time zone.')]
	locale: Annotated[str, Doc('Locale.')]
	phone_number: Annotated[str, Doc('Preferred telephone number.')]
	phone_number_verified: Annotated[
		bool,
		Doc('True if the phone number has been verified; otherwise false.'),
	]
	address: Annotated[str, Doc('Preferred postal address.')]
	updated_at: Annotated[str, Doc('Time the information was last updated.')]
	azp: Annotated[
		str,
		Doc('Authorized party - the party to which the ID Token was issued.'),
	]
	nonce: Annotated[
		str,
		Doc(
			"""
            Value used to associate a Client session with an ID Token
            (MAY also be used for nonce values in other applications of JWTs).
            """
		),
	]
	auth_time: Annotated[str, Doc('Time when the authentication occurred.')]
	at_hash: Annotated[str, Doc('Access Token hash value.')]
	c_hash: Annotated[str, Doc('Code hash value.')]
	acr: Annotated[str, Doc('Authentication Context Class Reference.')]
	amr: Annotated[str, Doc('Authentication Methods References.')]
	sub_jwk: Annotated[
		str,
		Doc('Public key used to check the signature of an ID Token.'),
	]
	cnf: Annotated[str, Doc('Confirmation.')]
	sip_from_tag: Annotated[
		str, Doc('SIP From tag header field parameter value.')
	]
	sip_date: Annotated[str, Doc('SIP Date header field value.')]
	sip_callid: Annotated[str, Doc('SIP Call-Id header field value.')]
	sip_cseq_num: Annotated[
		str, Doc('SIP CSeq numeric header field parameter value.')
	]
	sip_via_branch: Annotated[
		str, Doc('SIP Via branch header field parameter value.')
	]
	orig: Annotated[str, Doc('Originating Identity String.')]
	dest: Annotated[str, Doc('Destination Identity String.')]
	mky: Annotated[str, Doc('Media Key Fingerprint String.')]
	events: Annotated[str, Doc('Security Events.')]
	toe: Annotated[str, Doc('Time of Event.')]
	txn: Annotated[str, Doc('Transaction Identifier.')]
	rph: Annotated[str, Doc('Resource Priority Header Authorization.')]
	sid: Annotated[str, Doc('Session ID.')]
	vot: Annotated[str, Doc('Vector of Trust value.')]
	vtm: Annotated[str, Doc('Vector of Trust trustmark URL.')]
	attest: Annotated[
		str, Doc('Attestation level as defined in SHAKEN framework.')
	]
	origid: Annotated[
		str,
		Doc('Originating Identifier as defined in SHAKEN framework.'),
	]
	act: Annotated[str, Doc('Actor')]
	scope: Annotated[str, Doc('Scope Values')]
	client_id: Annotated[str, Doc('Client Identifier')]
	may_act: Annotated[
		str,
		Doc(
			"""
            Authorized Actor - the party that is authorized to become the
            actor.
            """
		),
	]
	jcard: Annotated[str, Doc('jCard data.')]
	at_use_nbr: Annotated[
		str,
		Doc('Number of API requests for which the access token can be used.'),
	]
	div: Annotated[str, Doc('Diverted Target of a Call.')]
	opt: Annotated[str, Doc('Original PASSporT (in Full Form).')]
	vc: Annotated[
		str,
		Doc('Verifiable Credential as specified in the W3C Recommendation.'),
	]
	vp: Annotated[
		str,
		Doc('Verifiable Presentation as specified in the W3C Recommendation.'),
	]
	sph: Annotated[str, Doc('SIP Priority header field.')]
	ace_profile: Annotated[
		str,
		Doc('The ACE profile a token is supposed to be used with.'),
	]
	cnonce: Annotated[
		str,
		Doc(
			"""
            "client-nonce". A nonce previously provided to the AS by the RS
            via the client. Used to verify token freshness when the RS cannot
            synchronize its clock with the AS.'
            """
		),
	]
	exi: Annotated[
		str,
		Doc(
			"""
            "Expires in". Lifetime of the token in seconds from the time the
            RS first sees it. Used to implement a weaker from of token
            expiration for devices that cannot synchronize their internal
            clocks.
            """
		),
	]
	roles: Annotated[str, Doc('Roles.')]
	groups: Annotated[str, Doc('Groups.')]
	entitlements: Annotated[str, Doc('Entitlements;')]
	token_introspection: Annotated[str, Doc('Token introspection response.')]
	eat_nonce: Annotated[str, Doc('Nonce.')]
	ueid: Annotated[str, Doc('The Universal Entity ID.')]
	sueids: Annotated[str, Doc('Semi-permanent UEIDs.')]
	oemid: Annotated[str, Doc('Hardware OEM ID.')]
	hwmodel: Annotated[str, Doc('Model identifier for hardware.')]
	hwversion: Annotated[str, Doc('Hardware Version Identifier.')]
	oemboot: Annotated[
		str,
		Doc('Indicates whether the software booted was OEM authorized.'),
	]
	dbgstat: Annotated[str, Doc('Indicates status of debug facilities.')]
	location: Annotated[str, Doc('The geographic location.')]
	eat_profile: Annotated[str, Doc('Indicates the EAT profile followed.')]
	submods: Annotated[str, Doc('The section containing submodules.')]
	uptime: Annotated[str, Doc('Uptime.')]
	bootcount: Annotated[
		str,
		Doc('The number times the entity or submodule has been booted.'),
	]
	bootseed: Annotated[str, Doc('Identifies a boot cycle.')]
	dloas: Annotated[
		str,
		Doc('Certifications received as Digital Letters of Approval.'),
	]
	swname: Annotated[str, Doc('The name of the software running in the entity.')]
	swversion: Annotated[
		str, Doc('The version of software running in the entity.')
	]
	manifests: Annotated[
		str,
		Doc('Manifests describing the software installed on the entity.'),
	]
	measurements: Annotated[
		str,
		Doc(
			"""
            Measurements of the software, memory configuration and such on the
            entity.
            """
		),
	]
	measres: Annotated[
		str,
		Doc(
			"""
            The results of comparing software measurements to reference values.
            """
		),
	]
	intuse: Annotated[str, Doc('Indicates intended use of the EAT.')]
	cdniv: Annotated[str, Doc('CDNI Claim Set Version.')]
	cdnicrit: Annotated[str, Doc('CDNI Critical Claims Set.')]
	cdniip: Annotated[str, Doc('CDNI IP Address.')]
	cdniuc: Annotated[str, Doc('CDNI URI Containe.')]
	cdniets: Annotated[
		str,
		Doc('CDNI Expiration Time Setting for Signed Token Renewal.'),
	]
	cdnistt: Annotated[
		str,
		Doc('CDNI Signed Token Transport Method for Signed Token Renewal.'),
	]
	cdnistd: Annotated[str, Doc('CDNI Signed Token Depth.')]
	sig_val_claims: Annotated[str, Doc('Signature Validation Token.')]
	authorization_details: Annotated[
		str,
		Doc(
			"""
            The claim authorization_details contains a JSON array of JSON
            objects representing the rights of the access token. Each JSON
            object contains the data to specify the authorization requirements
            for a certain type of resource.
            """
		),
	]
	verified_claims: Annotated[
		str,
		Doc(
			"""
            This container Claim is composed of the verification evidence
            related to a certain verification process and the corresponding
            Claims about the End-User which were verified in this process.
            """
		),
	]
	place_of_birth: Annotated[
		str,
		Doc('A structured Claim representing the End-Users place of birth.'),
	]
	nationalities: Annotated[
		str,
		Doc('String array representing the End-Users nationalities.'),
	]
	birth_family_name: Annotated[
		str,
		Doc(
			"""
            Family name(s) someone has when they were born, or at least from
            the time they were a child. This term can be used by a person who
            changes the family name(s) later in life for any reason. Note that
            in some cultures, people can have multiple family names or no
            family name; all can be present, with the names being separated by
            space characters.
            """
		),
	]
	birth_given_name: Annotated[
		str,
		Doc(
			"""
            Given name(s) someone has when they were born, or at least from
            the time they were a child. This term can be used by a person who
            changes the given name later in life for any reason. Note that in
            some cultures, people can have multiple given names; all can be
            present, with the names being separated by space characters.
            """
		),
	]
	birth_middle_name: Annotated[
		str,
		Doc(
			"""
            Middle name(s) someone has when they were born, or at least from
            the time they were a child. This term can be used by a person who
            changes the middle name later in life for any reason.
            Note that in some cultures, people can have multiple middle names;
            all can be present, with the names being separated by space
            characters. Also note that in some cultures, middle names are not
            used.
            """
		),
	]
	salutation: Annotated[str, Doc('End-Users salutation, e.g., "Mr.".')]
	title: Annotated[str, Doc('End-Users title, e.g., "Dr."')]
	msisdn: Annotated[
		str,
		Doc(
			"""
            End-Users mobile phone number formatted according to ITU-T
            recommendation.
            """
		),
	]
	also_known_as: Annotated[
		str,
		Doc(
			"""
            Stage name, religious name or any other type of alias/pseudonym
            with which a person is known in a specific context besides its
            legal name. This must be part of the applicable legislation and
            thus the trust framework (e.g., be an attribute on the identity
            card).
            """
		),
	]
	htm: Annotated[str, Doc('The HTTP method of the request')]
	htu: Annotated[
		str,
		Doc('The HTTP URI of the request (without query and fragment parts).'),
	]
	ath: Annotated[
		str,
		Doc(
			"""
            The base64url-encoded SHA-256 hash of the ASCII encoding of the
            associated access tokens value.
            """
		),
	]
	atc: Annotated[str, Doc('Authority Token Challenge.')]
	sub_id: Annotated[str, Doc('Subject Identifier.')]
	rcd: Annotated[str, Doc('Rich Call Data Information.')]
	rcdi: Annotated[str, Doc('Rich Call Data Integrity Information.')]
	crn: Annotated[str, Doc('Call Reason.')]
	msgi: Annotated[str, Doc('Message Integrity Information.')]
	_claim_names: Annotated[
		str,
		Doc(
			"""
            JSON object whose member names are the Claim Names for the
            Aggregated and Distributed Claims.
            """
		),
	]
	_claim_sources: Annotated[
		str,
		Doc(
			"""
            JSON object whose member names are referenced by the member values
            of the _claim_names member.
            """
		),
	]
	rdap_allowed_purposes: Annotated[
		str,
		Doc(
			"""
            This claim describes the set of RDAP query purposes that are
            available to an identity that is presented for access to a
            protected RDAP resource.
            """
		),
	]
	rdap_dnt_allowed: Annotated[
		str,
		Doc(
			"""
            This claim contains a JSON boolean literal that describes a
            "do not track" request for server-side tracking, logging, or
            recording of an identity that is presented for access to a
            protected RDAP resource.
            """
		),
	]
	geohash: Annotated[str, Doc('Geohash String or Array.')]
