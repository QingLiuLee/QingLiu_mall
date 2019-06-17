import React,{ Component } from "react"
import {Modal,Button} from 'antd'
/**
 * @author hui
 * @date 2019/6/17
 * @Description: Modal
 * 配置默认项
*/
export default class MyModal extends Modal {
    render(){
        let { onCancel, onSubmit, title, children,
            maskClosable,destroyOnClose,
            footer ,loading,disabled
        } = this.props;
        return  <Modal {...this.props}
                       maskClosable={maskClosable ? maskClosable : false}
                       destroyOnClose={destroyOnClose ? destroyOnClose : true}
                       title={title}
                       onCancel={onCancel}
                       footer={footer ? footer :[
                           <Button
                               loading={loading}
                               key={1}
                               type="primary"
                               onClick={onSubmit}
                               disabled={ disabled ? disabled : false }
                           >确定</Button>,
                           <Button key={2}  onClick={onCancel}>取消</Button>
                       ]}>
                    {children}
                </Modal>
    }
}

