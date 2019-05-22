import React,{Component} from 'react';
import { Table, Icon, Divider } from 'antd';
import ComTable from '../common/ComTable';
import SearchForm from '../search';

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商铺管理
*/
export default class Profile extends Component{
    constructor(props){
        super(props);
        this.state = {
            url:'/v1/merchant/staff/create/inner/info',
            refresh: 0,//table改变时对应刷新变化值
            postParam:{},
            getParam:{}
        }
    }

    componentDidMount = () => {
        this.setState({
            refresh:1
        },()=>{
            this.setState({
                refresh: 0
            })
        })
    }

    onSearch = (val)=>{

    }

    render (){
        const columns = [{
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            render: text => <a href="#">{text}</a>,
        }, {
            title: 'Age',
            dataIndex: 'age',
            key: 'age',
        }, {
            title: 'Address',
            dataIndex: 'address',
            key: 'address',
        }, {
            title: 'Action',
            key: 'action',
            render: (text, record) => (
                <span>
                  <a href="#">Action 一 {record.name}</a>
                  <Divider type="vertical" />
                  <a href="#">Delete</a>
                  <Divider type="vertical" />
                  <a href="#" className="ant-dropdown-link">
                    More actions <Icon type="down" />
                  </a>
                </span>
            ),
        }];

        const data = [{
            key: '1',
            name: 'John Brown',
            age: 32,
            address: 'New York No. 1 Lake Park',
        }, {
            key: '2',
            name: 'Jim Green',
            age: 42,
            address: 'London No. 1 Lake Park',
        }, {
            key: '3',
            name: 'Joe Black',
            age: 32,
            address: 'Sidney No. 1 Lake Park',
        }];

        return (
            <div className="lee-home">
                <div className="lee-home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="lee-home-table">
                    <Table columns={columns} dataSource={data} />

                    <ComTable
                        columns={columns}
                        url={this.state.url}
                        refresh={this.state.refresh}
                        postParam={this.state.postParam}
                        getParam={this.state.getParam}
                    />
                </div>
            </div>
        )
    }
}