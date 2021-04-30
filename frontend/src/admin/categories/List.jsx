import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import { categoryService } from '@/_services';

function List({ match }) {
    const { path } = match;
    const [categories, setCategories] = useState(null);

    useEffect(() => {
        categoryService.getAll().then(x => setCategories(x));
    }, []);

    function deleteCategory(id) {
        setCategories(categories.map(x => {
            if (x._id['$oid'] === id) { x.isDeleting = true; }
            return x;
        }));
        categoryService.delete(id).then(() => {
            setCategories(categories => categories.filter(x => x._id['$oid'] !== id));
        });
    }

    return (
        <div>
            <h1>Categories</h1>
            <p>All categories</p>
            <Link to={`${path}/add`} className="btn btn-sm btn-success mb-2">Add Category</Link>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th style={{ width: '27%' }}>Name</th>
                        <th style={{ width: '55%' }}>Description</th>
                        <th style={{ width: '18%' }}></th>
                    </tr>
                </thead>
                <tbody>
                    {categories && categories.map(category =>
                        <tr key={category._id['$oid']}>
                            <td>{category.name}</td>
                            <td>{category.desc}</td>
                            <td style={{ whiteSpace: 'nowrap' }}>
                                <Link to={`${path}/edit/${category._id['$oid']}`} className="btn btn-sm btn-primary mr-1">Edit</Link>
                                <button onClick={() => deleteCategory(category._id['$oid'])} className="btn btn-sm btn-danger" style={{ width: '60px' }} disabled={category.isDeleting}>
                                    {category.isDeleting 
                                        ? <span className="spinner-border spinner-border-sm"></span>
                                        : <span>Delete</span>
                                    }
                                </button>
                            </td>
                        </tr>
                    )}
                    {!categories &&
                        <tr>
                            <td colSpan="4" className="text-center">
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