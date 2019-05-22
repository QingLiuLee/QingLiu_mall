import React,{ Component } from "react"
import {Table,Pagination,Button,Checkbox,Popover} from 'antd'
import { post } from "../../utils/AxiosUtil";
const ButtonGroup = Button.Group;

/**
 * @author hui
 * @date 2018
 * @Description: table(显示|分页|隐藏显示列|鼠标移上显示|列可拖曳)
 */
class MyTable extends Component {
    constructor(props){
        super(props);

        this.state = {
            data: this.props.data ? this.props.data : [],
            pagination: {
                pageNo:1,
                pageSize:10
            },
            total: 0,
            size:'middle',
            border:this.props.border == false ? false : true,
            loading: false,

            newColumns:this.props.columnsProps ? this.props.columnsProps : this.props.columns,  //保存原始数组
            plainOptions:[], //checkbox数组
            visible:false,  //显示checkbox
            fieldOrder:null,
            orderField:null,
        };
    }

    //渲染后初始化
    componentDidMount(){
        if(this.props.columnsProps) {
            let plainOptions = [];
            let columnsProps = [...this.props.columnsProps];
            if (this.props.showBtn) {//默认有隐藏字段
                columnsProps.map(item => {
                    if (item.display == false) {
                        plainOptions.push({
                            title: item.title,
                            checked: false
                        });
                    } else {
                        plainOptions.push({
                            title: item.title,
                            checked: true
                        });
                    }
                });
                columnsProps = columnsProps.filter(item => item.display != false)
            } else {
                columnsProps.map(item => {
                    plainOptions.push({
                        title: item.title,
                        checked: true
                    });
                });
            }
            this.setState({
                plainOptions: plainOptions,
                newColumns: columnsProps
            })
        }
    }

    //选中事件
    onChecked = (val,e)=>{  //不刷新table
        let plainOptions = [...this.state.plainOptions];
        plainOptions.map((item) =>{
            if(item.title == val.title){
                item.checked = e.target.checked;
            }
        });

        this.props.columnsProps.map(item =>{  //每次操作都会有记录
            if(item.title == val.title){
                item.display = e.target.checked;
            }
        })

        let newColumns = [...this.props.columnsProps].filter(item => item.display != false)
        this.setState({newColumns:newColumns,plainOptions:plainOptions});
    }

    //获取数据
    fetch = (getParams,postParams)=>{
        this.setState({ loading: true });
        let postParam = {...this.state.pagination,total: true};

        if(Object.keys(postParams).length == 0){
            // console.log(postParams)
        }else{
            if(postParams.pageNo && postParams.pageSize){
                this.setState({
                    pagination:{
                        pageNo:postParams.pageNo,
                        pageSize:postParams.pageSize
                    }
                });
                postParam = {...postParams,total: true};
            }else{
                let size = this.state.pagination.pageSize;
                postParam = {pageNo:1,pageSize:size, total: true, ...postParams}
                this.setState({
                    pagination:{
                        pageNo:1,
                        pageSize:size
                    }
                });
            }
        }
        post(this.props.url, postParam, this.props.getParam).then(res => {
            let data = [];
            let total = 0;
            if (res.data){
                data = res.data.rows;
                total = res.data.total;
            }
            if(this.props.rowMerge!=undefined && this.props.rowMerge){
                data = this.rowMerge(res.data.rows);
            }
            this.setState({
                data: data,
                pagination:{...this.state.pagination},
                total:total,
                loading: false
            });
        }).catch(err => {
            this.setState({ loading: false });
            if(err.code){
                ProptModal.MyWarningModal(err.code + " : " + err.message);
            }else{
                console.log("table错误")
            }
        });
    }

    //查询|排序
    handleTableChange = (pageNo,pageSize,pagination)=>{
        if(pagination != null){
            this.setState({
                orderField:pagination.field,
                fieldOrder:pagination.order,
            });
            this.fetch({getParam: this.props.getParam}, {
                ...this.props.postParam,
                pageNo: this.state.pagination.pageNo,
                pageSize: this.state.pagination.pageSize,
                total:this.state.total,
                attributeNamesForOrderBy :{[pagination.field]:pagination.order}
            });
        }
        else{
            if(!this.state.orderField || !this.state.fieldOrder){
                this.fetch({getParam: this.props.getParam}, {
                    ...this.props.postParam,
                    pageNo: pageNo,
                    pageSize: pageSize,
                });
            }
            else{
                this.fetch({getParam: this.props.getParam}, {
                    ...this.props.postParam,
                    pageNo: pageNo,
                    pageSize: pageSize,
                    attributeNamesForOrderBy :{[this.state.orderField]:this.state.fieldOrder},
                });
            }
        }
    }

    //分页
    changeSize = (pageNo, pageSize)=>{
        this.setState({
            pagination:{
                pageNo: pageNo,
                pageSize: pageSize
            }
        });
        this.handleTableChange(pageNo,pageSize)
    }

    //table变化后刷新
    componentWillReceiveProps(){
        if(this.props.refresh != 0 && this.props.refresh!=undefined){
            this.fetch(this.props.getParam,this.props.postParam);
        }
    }

    getData=()=>{
        return this.state.data;
    }

    handleResize = index => (e, { size }) => {
        this.setState(({ newColumns }) => {
            const nextColumns = [...newColumns];
            nextColumns[index] = {
                ...nextColumns[index],
                width: size.width,
            };
            return { newColumns: nextColumns };
        });
    };

    render() {
        const newColumns = this.state.newColumns.map((col, index) => ({
            ...col,
            width: this.props.scrollWidth ? this.props.scrollWidth[index] : col.width,
        }));

        const content = (
            <div className="table-checkbox">
                {
                    [...this.state.plainOptions].map((item)=>{
                        if(item.checked == true){
                            return <Checkbox checked onChange={this.onChecked.bind(this,item)} key={item + Math.random()*10000} style={{display: 'block'}}>{item.title}</Checkbox>
                        }else{
                            return <Checkbox onChange={this.onChecked.bind(this,item)} key={item + Math.random()*10000} style={{display: 'block'}}>{item.title}</Checkbox>
                        }
                    })
                }
            </div>
        );

        let top = 0;
        if(this.props.showBtn){if(this.props.top){top = 0;} else{top = -40;}}
        return (
            <div style={{position:'relative',top:top + 'px'}} className="com-table-all">
                <div style={{display:this.props.showBtn ? 'inline-block':'none',height:'30px',marginBottom: '10px'}}>
                    <div className="table-btn">
                        <Popover
                            title="隐藏/显示列"
                            placement="bottomRight"
                            trigger="click"
                            arrowPointAtCenter
                            content={content}
                            visible={this.state.visible}
                            onVisibleChange={(visible) => {this.setState({ visible });}}
                            getPopupContainer={(node)=> node.parentNode}
                        >
                            <Button type="dashed" icon="table" >隐藏/显示</Button>
                        </Popover>
                    </div>
                </div>
                {/*<div id="table-popover"></div>*/}
                <Table
                    {...this.props}
                    bordered = {this.state.border}
                    size = {this.state.size}
                    pagination = {false}
                    loading = {this.state.loading}
                    dataSource={this.state.data}
                    refresh = {this.state.refresh}
                    onChange={this.handleTableChange}
                    url = {this.props.url}
                    rowKey={this.props.rowKeys != null ? this.props.rowKeys : record => record.id}
                    columns={newColumns}
                    components={this.props.isResize ? components : undefined}

                    plainOptions = {this.state.plainOptions}
                />

                {this.props.display ? null :
                    <Pagination
                        pagination="bottom"
                        showSizeChanger={true}
                        showQuickJumper={true}
                        // hideOnSinglePage={true}  //默认只有一页不显示分页

                        current={this.state.pagination.pageNo}
                        pageSize={this.state.pagination.pageSize}

                        total={this.state.total}
                        showTotal={(total, range) => `共有 ${total} 条记录`}
                        pageSizeOptions={this.props.pageSizeOpt==undefined?['10', '20', '30', '50', '100']:this.props.pageSizeOpt}

                        onChange={this.changeSize}
                        onShowSizeChange={this.changeSize}

                    />
                }
            </div>
        );
    }
}

export default MyTable