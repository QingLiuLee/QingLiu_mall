import React from 'react';
import { Input, Button } from 'antd';
import {getLocalStorage} from "../../../utils/localStorage";

class SearchForm extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            staff_code: getLocalStorage('staff_code'),
        }
    }

    onSearch = ()=>{
        this.props.onSearch(this.state);
    }

    onReset = ()=>{
        this.setState({
            userName:''
        })
    }

    render() {
        const { staff_code } = this.state;

        return (
            <div className="ql-search-div">
                <div>
                    <label className="label-red">商铺管理员编码</label>
                    <Input
                        style={{width:150}}
                        placeholder="请输入"
                        value={staff_code}
                        onChange={(e)=>this.setState({staff_code:e.target.value})}
                    />
                </div>
                <Button type="primary" onClick={this.onSearch}>查询</Button>
                <Button type="primary" ghost onClick={this.onReset}>重置</Button>
            </div>
        );
    }
}

export default SearchForm;