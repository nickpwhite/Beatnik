# typed: strict

module RSpotify
  class Base
    sig do
      params(
        ids: T.any(String, T::Array[String]),
        type: String,
        market: String
      )
      .returns(
        T.any(
          Album,
          Artist,
          Track,
          User,
          T::Array[Album],
          T::Array[Artist],
          T::Array[Track]
        )
      )
    end
    def self.find(ids, type, market: nil); end

    sig do
      params(
        query: String,
        types: String,
        limit: Integer,
        offset: Integer,
        market: T.nilable(T.any(String, {from: User}))
      )
      .returns(
        T.any(
          T::Array[Album],
          T::Array[Artist],
          T::Array[Track],
          T::Array[Playlist],
          T::Array[Base],
        )
      )
    end
    def self.search(query, types, limit: 20, offset: 0, market: nil); end

    sig {returns(T::Hash[String, String])}
    def external_urls; end
  end

  class Album < Base
    sig do
      params(
        ids: T.any(String, T::Array[String]),
        market: String
      )
      .returns(
        T.any(Album, T::Array[Album])
      )
    end
    def self.find(ids, market: nil); end

    sig do
      params(
        query: String,
        limit: Integer,
        offset: Integer,
        market: T.nilable(T.any(String, {from: User}))
      )
      .returns(
        T::Array[Album]
      )
    end
    def self.search(query, limit: 20, offset: 0, market: nil); end

    sig {returns(T.nilable(T::Array[Artist]))}
    def artists; end

    sig {returns(String)}
    def name; end
  end

  class Artist < Base
    sig {returns(String)}
    def name; end
  end

  class Playlist < Base
  end

  class Track < Base
    sig do
      params(
        ids: T.any(String, T::Array[String]),
        market: String
      )
      .returns(
        T.any(Track, T::Array[Track])
      )
    end
    def self.find(ids, market: nil); end

    sig do
      params(
        query: String,
        limit: Integer,
        offset: Integer,
        market: T.nilable(T.any(String, {from: User}))
      )
      .returns(
        T::Array[Track]
      )
    end
    def self.search(query, limit: 20, offset: 0, market: nil); end

    sig {returns(T.nilable(Album))}
    def album; end

    sig {returns(T.nilable(T::Array[Artist]))}
    def artists; end

    sig {returns(String)}
    def name; end
  end

  class User < Base
  end
end
