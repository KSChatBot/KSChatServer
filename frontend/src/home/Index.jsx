import React, { useEffect, useState } from 'react';

import { apiService } from '@/_services';

import { BlockList } from '@/_components';

function Home() {
    const [apis, setApis] = useState(null);
    const [searchInput, setSearchInput] = useState('');
    const [defaultApis, setDefaultApis] = useState(null);
    const [listStatus, setListStatus] = useState('default');
    const [searchKeyword, setSearchKeyword] = useState('');

    const changeSearchInput = (e) => {
        setSearchInput(e.target.value);
    }

    const filteringApi = () => {
        if(searchInput) {
            setApis(defaultApis.filter(api => (api.api_name.indexOf(searchInput) != -1 || api.api_desc.indexOf(searchInput) != -1)));
            setSearchKeyword(searchInput);
            setListStatus('search');
        } else {
            setApis(defaultApis);
            setListStatus('default');
        }
        setSearchInput('');
    }

    const enterInput = (e) => {
        if(e.key === 'Enter') filteringApi();
    }

    initWebchat(
        "https://endpoint-bot.ks-cognigy.com/e5d61dac0499b1583ed3cf6758e1fa1ee4c45a9a12552d97338e24515517bfd6"
    ).then((webchat) => {window.webchat = webchat;});
    
    useEffect(() => {
        apiService.getAll().then(x => {setApis(x); setDefaultApis(x);});
    }, []);
    
    return (
        <React.Fragment>
            <div className="image-cover main_banner" style={{background: '#003783'}} data-overlay="0">
                <div className="container">
                    <div className="row align-items-center">
                        <div className="col-lg-6 col-md-6 col-sm-12">
                            <div className="banner-search-2 transparent">
                                <h1 className="big-header-capt cl_2 mb-2">Searching Api with KS Server</h1>
                                <p>Api를 검색해 보세요.</p>
                                <div className="mt-4">
                                    <div className="banner-search shadow_high">
                                        <div className="search_api_wrapping">
                                            <div className="row">
                                                <div className="col-lg-10 col-md-10 col-sm-12">
                                                    <div className="form-group">
                                                        <div className="input-with-icon">
                                                            <input
                                                                id="searchApi"
                                                                type="text"
                                                                className="form-control"
                                                                placeholder="Keyword"
                                                                onChange={changeSearchInput}
                                                                onKeyPress={enterInput}
                                                                value={searchInput} />
                                                            <img src="https://themezhub.net/learnup-demo-2/learnup/assets/img/search.svg" className="search-icon" />
                                                        </div>
                                                    </div>
                                                </div>
                                                <div className="col-lg-2 col-md-2 col-sm-12 pl-0">
                                                    <div className="form-group none">
                                                        <a className="btn search-btn full-width" onClick={filteringApi}>Go</a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-lg-6 col-md-6 col-sm-12">
                            <div className="flixio pt-5">
                                <img className="img-fluid" src="https://themezhub.net/learnup-demo-2/learnup/assets/img/edu_2.png" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <section className="gray-bg">
                <div className="container">
                    <div className="row justify-content-center">
                        <div className="col-lg-5 col-md-6 col-sm-12">
                            <div className="sec-heading center">
                                <p>API 목록</p>
                                {listStatus==='search' ?
                                    <h2><span className="theme-cl">{searchKeyword}</span> 검색 결과 : 총 {apis.length} 개</h2> :
                                    <h2><span className="theme-cl">주요</span> API</h2>
                                }
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        {apis && (apis.length >= 6?
                            apis.slice(0, 5).map((api, index) =>
                                <BlockList name={api.api_name} desc={api.api_desc} key={api._id['$oid']} />
                            ) : apis.map((api, index) =>
                                <BlockList name={api.api_name} desc={api.api_desc} key={api._id['$oid']} />
                            ).concat([...Array(6-apis.length)].map((n, index) =>
                                <BlockList name={`Temp${index}`} desc={'none'} key={apis.length + index} />
                            ))
                        )}
                    </div>
                </div>
            </section>
        </React.Fragment>
    );
}

export { Home };