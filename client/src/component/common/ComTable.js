import React,{ Component } from "react"
import {Table,Pagination,Button,Checkbox,Popover} from 'antd'
import { post } from "../../utils/axiosUtil";
import { offset,getSize } from '../../utils/document'
/**
 * @author hui
 * @date 2018
 * @Description: table(显示|分页|隐藏显示列|鼠标移上显示|列可拖曳)
 */
class MyTable extends Component {
    constructor(props){
        super(props);

        this.state = {
            data: [],
            pagination: {
                pageNo:1,
                pageSize:10
            },
            total: 0,
            size:'middle',
            border: true,
            loading: false,

            newColumns:this.props.columnsProps ? this.props.columnsProps : this.props.columns,  //保存原始数组
            plainOptions:[], //checkbox数组
            visible:false,  //显示checkbox

            fieldOrder:null,
            orderField:null,

            tableHeight: 0
        };
    }

    // 设置高
    setHeight = height => {
        let tableHeight = 0;
        // 获取table头部的高度
        let tableTopHeight = 0;
        if (this.tableRef) {
            tableTopHeight = this.tableRef.querySelector(".ant-table-thead")
                .clientHeight;
        }
        if (height > 0) {
            tableHeight = height;
        } else {
            const offsetTop = offset(this.tableRef).top;
            tableHeight = getSize().windowH - offsetTop - tableTopHeight - 55
        }
        this.setState({
            tableHeight
        });
    };

    //渲染后初始化
    componentDidMount(){
        let { columnsProps } = this.props;
        if(columnsProps) {
            let plainOptions = [];
            columnsProps.map(item => {
                plainOptions.push({
                    title: item.title,
                    checked: item.display ? false : true
                });
            });
            // 过滤默认有隐藏字段
            columnsProps = columnsProps.filter(item => item.display !== false)
            this.setState({
                plainOptions: plainOptions,
                newColumns: columnsProps
            })
        }

        // 设置scroolY
        if(this.props.scroll && this.props.scroll.y === 0){
            this.setHeight(0)
        }
    }

    //选中事件
    onChecked = (val,e)=>{  //不刷新table
        let { plainOptions, columnsProps } = [...this.state.plainOptions];
        plainOptions.map((item, index) =>{
            if(item.title === val.title){
                item.checked = e.target.checked;
                columnsProps[index].display = e.target.checked;
            }
        });
        let newColumns = columnsProps.filter(item => item.display !== false)
        this.setState({newColumns, plainOptions});
    }

    //获取数据
    fetch = (getParams,postParams)=>{
        this.setState({ loading: true });
        let { data, pagination }  = this.state
        if(data.length > 0){
            postParams = {
                ...postParams,
                limit: postParams.pageSize,
                last_id: data[data.length - 1]._id
            }
            pagination = {
                pageNo: postParams.pageNo,
                    pageSize: postParams.pageSize,
            }
        }
        post(this.props.url, postParams, getParams).then(res => {
            if (res.data){
                this.setState({
                    pagination,
                    data: res.data.list,
                    total: res.data.count,
                    loading: false
                });
            }
        }).catch(err => {
            this.setState({ loading: false });
            if(!err.code){
                console.log("table错误")
            }
        });
    }

    //查询|排序
    handleTableChange = (pageNo,pageSize,pagination)=>{
        /*if(pagination != null){
            this.setState({
                orderField:pagination.field,
                fieldOrder:pagination.order,
            });
            this.fetch({getParam: this.props.getParam}, {
                ...this.props.postParam,
                ...this.state.pagination,
                total:this.state.total,
                attributeNamesForOrderBy :{[pagination.field]:pagination.order}
            });
        }
        else{*/
            this.fetch({getParam: this.props.getParam}, {
                ...this.props.postParam,
                ...pagination
                // attributeNamesForOrderBy : !this.state.orderField || !this.state.fieldOrder ? {} : {[this.state.orderField]:this.state.fieldOrder}
            });
        // }
    }

    //分页
    changeSize = (pageNo, pageSize)=>{
        let self = this;
        const oldPageNo = self.state.pagination.pageNo
        const curNum = pageNo > oldPageNo ?  pageNo - oldPageNo : oldPageNo - pageNo
        const turned = pageNo > oldPageNo ? 1 : -1
        const pagination = {
            pageNo: pageNo,
            pageSize: pageSize,
            skip: (curNum - 1) * pageSize,
            turned
        }
        this.handleTableChange(pageNo, pageSize, pagination)
    }

    //table变化后刷新
    componentWillReceiveProps(){
        if(this.props.refresh != 0 && this.props.refresh!=undefined){
            this.fetch(this.props.getParam,this.props.postParam);
            // 设置scroolY
            /*if(this.props.scroll && this.props.scroll.y){
                this.setHeight(0)
            }*/
        }
    }

    getData=()=>{
        console.log(this.state.data);
        return this.state.data;
    }

    render() {
        const {
            newColumns, plainOptions, visible,
            border, size, loading, data, refresh,
            total, pagination,
            tableHeight
        } = this.state;
        const {
            columnsProps, hasOpearBtn,
            url, rowKey,pageSizeOpt, newDatas,
            scroll
        } = this.props;

        const content = (
            <div className="table-checkbox">
                {
                    [...plainOptions].map((item, index)=>{
                        return <Checkbox
                            checked={item.checked}
                            onChange={this.onChecked.bind(this,item)}
                            key={index}
                            style={{display: 'block'}}
                        >{item.title}</Checkbox>
                    })
                }
            </div>
        );

        const top = columnsProps && hasOpearBtn ? -40 : 0;
        return (
            <div style={{position:'relative',marginTop:top + 'px'}} className="com-table-all" ref={ref => {this.tableRef = ref;}}>
                <div style={{display:columnsProps ? 'inline-block':'none',height:'30px',marginBottom: '10px'}}>
                    <div className="table-btn">
                        <Popover
                            title="隐藏/显示列"
                            placement="bottomRight"
                            trigger="click"
                            arrowPointAtCenter
                            content={content}
                            visible={visible}
                            onVisibleChange={(visible) => {this.setState({ visible });}}
                            getPopupContainer={(node)=> node.parentNode}
                        >
                            <Button type="dashed" icon="table" >隐藏/显示</Button>
                        </Popover>
                    </div>
                </div>

                <Table
                    {...this.props}
                    bordered = {border}
                    size = {size}
                    pagination = {false}
                    loading = {loading}
                    dataSource={newDatas ? newDatas : data}
                    refresh = {refresh}
                    onChange={this.handleTableChange}
                    url = {url}
                    rowKey={rowKey ? rowKey : record => record._id}
                    columns={newColumns}
                    plainOptions = {plainOptions}

                    scroll={{
                        ...scroll,
                        y: data && data[0] && scroll && scroll.y === 0 ? tableHeight : 0
                    }}
                />

                {this.props.display ? null :
                    <Pagination
                        style={{marginTop: 10}}
                        pagination="bottom"
                        showSizeChanger={true}
                        showQuickJumper={true}
                        // hideOnSinglePage={true}  //默认只有一页不显示分页

                        current={pagination.pageNo}
                        pageSize={pagination.pageSize}

                        total={total}
                        showTotal={(total, range) => `共有 ${total} 条记录`}
                        pageSizeOptions={pageSizeOpt == undefined ? ['10', '20', '30', '50', '100'] : pageSizeOpt }

                        onChange={this.changeSize}
                        onShowSizeChange={this.changeSize}

                    />
                }
            </div>
        );
    }
}

export default MyTable
