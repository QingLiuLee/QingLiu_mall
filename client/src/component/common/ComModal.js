import React,{ Component } from "react"
import {Modal,Button} from 'antd'

/**
 * liuhuihui
 * Modal
 */
export default class MyModal extends Modal {
    render(){
        let { onCancel, onSubmit, title, children, footer ,loading} = this.props;
        return  <Modal maskClosable={false} {...this.props}
                       destroyOnClose
                       title={title}
                       onCancel={onCancel}
                       footer={this.props.footer ? this.props.footer :[
                           <Button loading={loading} key={1} type="primary" onClick={onSubmit}>确定</Button>,
                           <Button key={2}  onClick={onCancel}>取消</Button>
                       ]}>
                    {children}
                </Modal>
    }
}

