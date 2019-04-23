//合并所有reducers,并且返回
import { combineReducers } from 'redux';
import { login } from  './login.redux';

export default combineReducers ({login})