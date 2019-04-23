//合并所有reducers,并且返回
import { createStore, applyMiddleware, compose } from 'redux';
import reducer from "./combineReducers";
import thunk from 'redux-thunk';

const store = createStore(reducer,compose(
    applyMiddleware(thunk),
    window.devToolsExtension ? window.devToolsExtension():f=>f
));

export default store;