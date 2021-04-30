import config from 'config';
import { fetchWrapper } from '@/_helpers';

const baseUrl = `${config.apiUrl}/api/categories`;

export const categoryService = {
    getAll,
    getById,
    create,
    update,
    delete: _delete
};

function getAll() {
    return fetchWrapper.get(baseUrl);
}

function getById(id) {
    return fetchWrapper.get(`${baseUrl}/${id}`);
}

function create(params) {
    return fetchWrapper.post(`${baseUrl}`, params);
    console.log('api_contents 등록 성공....');
}

function update(id, params) {
    return fetchWrapper.put(`${baseUrl}/${id}`, params)
        .then(user => user);
}

// prefixed with underscore because 'delete' is a reserved word in javascript
function _delete(id) {
    return fetchWrapper.delete(`${baseUrl}/${id}`)
        .then(x => x);
}
