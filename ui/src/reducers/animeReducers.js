import {
  ANIME_DOWNLOAD_FAIL,
  ANIME_DOWNLOAD_REQUEST,
  ANIME_DOWNLOAD_SUCCESS,
  ANIME_EPISODE_ADD_FAIL,
  ANIME_EPISODE_ADD_REQUEST,
  ANIME_EPISODE_ADD_SUCCESS,
  ANIME_SEARCH_CLEAR,
  ANIME_SEARCH_FAIL,
  ANIME_SEARCH_REQUEST,
  ANIME_SEARCH_SUCCESS,
  ANIME_STREAM_CLEAR,
  ANIME_STREAM_DETAILS_CLEAR,
  ANIME_STREAM_DETAILS_FAIL,
  ANIME_STREAM_DETAILS_REQUEST,
  ANIME_STREAM_DETAILS_SUCCESS,
  ANIME_STREAM_EXTERNAL_CLEAR,
  ANIME_STREAM_EXTERNAL_FAIL,
  ANIME_STREAM_EXTERNAL_REQUEST,
  ANIME_STREAM_EXTERNAL_SUCCESS,
  ANIME_STREAM_URL_CLEAR,
  ANIME_STREAM_URL_FAIL,
  ANIME_STREAM_URL_REQUEST,
  ANIME_STREAM_URL_SUCCESS,
  DOWNLOAD_LIBRARY_FAIL,
  DOWNLOAD_LIBRARY_REQUEST,
  DOWNLOAD_LIBRARY_SUCCESS,
} from "../constants/animeConstants";

export const animeSearchListReducer = (state = { animes: null }, action) => {
  switch (action.type) {
    case ANIME_SEARCH_REQUEST:
      return {
        loading: true,
        animes: [],
      };

    case ANIME_SEARCH_SUCCESS:
      return { loading: false, animes: action.payload };

    case ANIME_SEARCH_FAIL:
      return { loading: false, error: action.payload };
    case ANIME_SEARCH_CLEAR:
      return { loading: false, animes: null };

    default:
      return state;
  }
};

export const animeEpisodeReducer = (state = {}, action) => {
  switch (action.type) {
    case ANIME_EPISODE_ADD_REQUEST:
      return { loading: false, details: action.payload };

    case ANIME_EPISODE_ADD_SUCCESS:
      return { loading: false, details: action.payload };

    case ANIME_EPISODE_ADD_FAIL:
      return { loading: false, details: action.payload };

    default:
      return state;
  }
};
export const animeEpUrlReducer = (
  state = {
    loading: null,
  },
  action
) => {
  switch (action.type) {
    case ANIME_STREAM_URL_REQUEST:
      return { loading: true, url: action.payload };

    case ANIME_STREAM_URL_SUCCESS:
      return { loading: false, url: action.payload };

    case ANIME_STREAM_URL_FAIL:
      return { loading: false, url: action.payload };
    case ANIME_STREAM_URL_CLEAR:
      return { loading: false, url: "" };

    default:
      return state;
  }
};

//StreamDetails
export const animeStreamDetailsReducer = (
  state = { details: null },
  action
) => {
  switch (action.type) {
    case ANIME_STREAM_DETAILS_REQUEST:
      return {
        loading: true,
        details: null,
      };

    case ANIME_STREAM_DETAILS_SUCCESS:
      return { loading: false, details: action.payload };

    case ANIME_STREAM_DETAILS_FAIL:
      return { loading: false, error: action.payload };
    case ANIME_STREAM_DETAILS_CLEAR:
      return { loading: false, details: null };

    default:
      return state;
  }
};

//Stream
export const animeStreamReducer = (state = { details: null }, action) => {
  switch (action.type) {
    case ANIME_STREAM_EXTERNAL_REQUEST:
      return {
        loading: true,
        details: null,
      };

    case ANIME_STREAM_EXTERNAL_SUCCESS:
      return { loading: false, details: action.payload };

    case ANIME_STREAM_EXTERNAL_FAIL:
      return { loading: false, error: action.payload };
    case ANIME_STREAM_EXTERNAL_CLEAR:
      return { loading: false, details: null };

    default:
      return state;
  }
};
export const animeDownloadReducer = (state = { details: null }, action) => {
  switch (action.type) {
    case DOWNLOAD_LIBRARY_REQUEST:
      return {
        loading: true,
        details: null,
      };

    case DOWNLOAD_LIBRARY_SUCCESS:
      return { loading: false, details: action.payload };

    case DOWNLOAD_LIBRARY_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
