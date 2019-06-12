import React,{Component} from 'react';
import { Input, Button } from 'antd';

class SearchForm extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            userName:'hui'
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
        const { userName } = this.state;

        return (
            <div className="ql-search-div">
                <div>
                    {/*<label><em className="red">*</em>学年学期</label>*/}
                    <label>用户名</label>
                    <Input
                        style={{width:150}}
                        placeholder="Username"
                        value={userName}
                        onClick={(e)=>this.setState({userName:e.target.value})}
                    />
                </div>
                <Button type="primary" onClick={this.onSearch}>查询</Button>
                <Button type="primary" ghost onClick={this.onReset}>重置</Button>
            </div>
        );
    }
}

export default SearchForm;