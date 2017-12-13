module Main exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)
import Navigation exposing (Location, newUrl)



main =
  Navigation.program urlChange
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    }

-- MODEL
type Page
  = Home
  | Music

type alias MusicInfo = 
  { musicType : String
  , title : String
  , artist : String
  , art : String
  , album : Maybe String
  }

type alias Model 
  = { currentPage : Page
    , musicInfo : Maybe MusicInfo
    }



init : Location -> (Model, Cmd Msg)
init location =
  let
      page =
        case location.pathname of
          "/music/" ->
            Music
          _ ->
            Home
  in
      (Model page Nothing
      , getMusic location.search)


-- UPDATE

type Msg 
  = GoTo Page
  | LinkTo String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    GoTo page -> 
      ({ model | currentPage = page }, Cmd.none)

    LinkTo path ->
      (model, newUrl path)



-- VIEW

renderMenu : Model -> Html Msg
renderMenu model =
  div []
      [ button [ onClick (LinkTo "/home/") ] [ text "Home" ] 
      , button [ onClick (LinkTo "/music/") ] [ text "Music" ] 
      ]

renderPage : Model -> Html Msg
renderPage model =
  let
      pageContent =
        case model.currentPage of
          Home -> 
            text "Home"
          Music ->
            text "Music"
  in
      div [] [ pageContent ]

view : Model -> Html Msg
view model =
  div []
      [ h1 [] [ text "Beatnik" ]
      , renderMenu model
      , renderPage model
      ]


-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- HTTP

getMusic : String -> Cmd Msg
getMusic query =
  let
      q = parseQuery query
  in
      case q of
        "" ->
          Cmd.none

        _ ->
          Cmd.none


-- NAVIGATION

urlChange : Location -> Msg
urlChange location =
  case location.pathname of
    "/music/" ->
      GoTo Music
    _ ->
      GoTo Home


-- HELPERS

parseQuery : String -> String
parseQuery query =
  String.dropLeft 3 query
