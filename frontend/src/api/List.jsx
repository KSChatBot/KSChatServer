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

    function copy(content) {
        const tempInput = document.createElement('textarea');
        tempInput.value = content;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
    }

    return (
        <div>
            <h1>Api_Contents</h1>
            <p>All api contents</p>
            <Link to={`${path}/add`} className="btn btn-sm btn-success mb-2">Add Api</Link>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th style={{ width: '18%' }}>Name</th>
                        <th style={{ width: '18%' }}>Description</th>
                        <th style={{ width: '18%' }}>Key</th>
                        <th style={{ width: '18%' }}>Endpoint</th>
                        <th style={{ width: '14%' }}>DataFormat</th>
                        <th style={{ width: '14%' }}></th>
                    </tr>
                </thead>
                <tbody>
                    {apis && apis.map(api =>
                        <tr key={api._id['$oid']}>
                            <td>{api.api_name}</td>
                            <td>{api.api_desc}</td>
                            <td>{api.api_key}<button className="btn btn-sm" onClick={() => copy(api.api_key)}>Copy</button></td>
                            <td>{api.api_endpoint}<button className="btn btn-sm" onClick={() => copy(api.api_endpoint)}>Copy</button></td>
                            <td>{api.api_data_format}</td>
                            <td className="text-center" style={{ whiteSpace: 'nowrap' }}>
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