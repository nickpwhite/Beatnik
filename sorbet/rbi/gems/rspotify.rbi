# This file is autogenerated. Do not edit it by hand. Regenerate it with:
#   srb rbi gems

# typed: strict
#
# If you would like to make changes to this file, great! Please create the gem's shim here:
#
#   https://github.com/sorbet/sorbet-typed/new/master?filename=lib/rspotify/all/rspotify.rbi
#
# rspotify-2.10.2

module RSpotify
  def self.auth_header; end
  def self.authenticate(client_id, client_secret); end
  def self.client_token; end
  def self.delete(path, *params); end
  def self.get(path, *params); end
  def self.get_headers(params); end
  def self.post(path, *params); end
  def self.put(path, *params); end
  def self.raw_response; end
  def self.raw_response=(arg0); end
  def self.request_was_user_authenticated?(*params); end
  def self.resolve_auth_request(user_id, url); end
  def self.retry_connection(verb, url, params); end
  def self.send_request(verb, path, *params); end
end
class RSpotify::MissingAuthentication < StandardError
end
