import React from 'react';

const BlockList = ({ name, desc, img }) => {
    return (
        <React.Fragment>
            <div className="col-xl-6 col-lg-12 col-md-12 col-sm-12">
                <div className="api_block_list_layout">
                    <div className="api_block_thumb"><img src={img}></img></div>
                    <div className="list_layout_api_caption">
                        <div className="api_block_body">
                            <h4 className="api_name">{name}</h4>
                            <div className="api_desc">{desc}</div>
                        </div>
                    </div>
                </div>
            </div>
        </React.Fragment>
    );
};

export { BlockList };