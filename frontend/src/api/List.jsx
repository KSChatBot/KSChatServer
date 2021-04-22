import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import { apiService } from '@/_services';

function List({ match }) {
    const { path } = match;
    const [apis, setApis] = useState(null);

    useEffect(() => {
        apiService.getAll().then(x => setApis(x));
    }, []);

    function deleteApi(id) {
        setApis(apis.map(x => {
            if (x._id['$oid'] === id) { x.isDeleting = true; }
            return x;
        }));
        apiService.delete(id).then(() => {
            setApis(apis => apis.filter(x => x._id['$oid'] !== id));
        });
    }

    return (
        <div className="pt20">
            <h1>Api_Contents</h1>
            <p>All api contents</p>
            <Link to={`${path}/add`} className="btn btn-sm btn-success mb-2">Add Api</Link>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th style={{ width: '20%' }}>Name</th>
                        <th style={{ width: '20%' }}>Description</th>
                        <th style={{ width: '20%' }}>Key</th>
                        <th style={{ width: '20%' }}>Endpoint</th>
                        <th style={{ width: '10%' }}>DataFormat</th>
                        <th style={{ width: '10%' }}></th>
                    </tr>
                </thead>
                <tbody>
                    {apis && apis.map(api =>
                        <tr key={api._id['$oid']}>
                            <td>{api.api_name}</td>
                            <td>{api.api_desc}</td>
                            <td>{api.api_key}{/*<button className="btn btn-sm" onClick={}>Copy</button>*/}</td>
                            <td>{api.api_endpoint}</td>
                            <td>{api.api_data_format}</td>
                            <td style={{ whiteSpace: 'nowrap' }}>
                                <Link to={`${path}/edit/${api._id['$oid']}`} className="btn btn-sm btn-primary mr-1">Edit</Link>
                                <button onClick={() => deleteApi(api._id['$oid'])} className="btn btn-sm btn-danger" style={{ width: '60px' }} disabled={api.isDeleting}>
                                    {api.isDeleting 
                                        ? <span className="spinner-border spinner-border-sm"></span>
                                        : <span>Delete</span>
                                    }
                                </button>
                            </td>
                        </tr>
                    )}
                    {!apis &&
                        <tr>
                            <td colSpan="6" className="text-center">
                                <span className="spinner-border spinner-border-lg align-center"></span>
                            </td>
                        </tr>
                    }
                </tbody>
            </table>
        </div>
    );
}

export { List };