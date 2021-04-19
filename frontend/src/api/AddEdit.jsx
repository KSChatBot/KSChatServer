import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';

import { apiService, alertService } from '@/_services';

function AddEdit({ history, match }) {
    const { id } = match.params;
    const isAddMode = !id;
    
    const initialValues = {
        api_name: '',
        api_desc: '',
        api_key: '',
        api_endpoint: '',
        api_data_format: ''
    };

    const validationSchema = Yup.object().shape({
        api_name: Yup.string()
            .required('api 이름이 필요합니다.'),
        api_desc: Yup.string()
            .required('api 에 대한 설명이 필요합니다.'),
        api_key: Yup.string()
            .required('api key 가 필요합니다.'),
        api_endpoint: Yup.string()
            .required('api endpoint 가 필요합니다.'),
        api_data_format: Yup.string()
            .required('api data format 이 필요합니다.'),
    });

    function onSubmit(fields, { setStatus, setSubmitting }) {
        setStatus();
        if (isAddMode) {
            createApi(fields, setSubmitting);
        } else {
            updateApi(id, fields, setSubmitting);
        }
    }

    function createApi(fields, setSubmitting) {
        apiService.create(fields)
            .then(() => {
                alertService.success('Api added successfully', { keepAfterRouteChange: true });
                history.push('.');
            })
            .catch(error => {
                setSubmitting(false);
                alertService.error(error);
            });
    }

    function updateApi(id, fields, setSubmitting) {
        apiService.update(id, fields)
            .then(() => {
                alertService.success('Update successful', { keepAfterRouteChange: true });
                history.push('..');
            })
            .catch(error => {
                setSubmitting(false);
                alertService.error(error);
            });
    }

    return (
        <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
            {({ errors, touched, isSubmitting, setFieldValue }) => {
                useEffect(() => {
                    if (!isAddMode) {
                        // get user and set form fields
                        apiService.getById(id).then(api => {
                            const fields = ['api_name', 'api_desc', 'api_key', 'api_endpoint', 'api_data_format'];
                            fields.forEach(field => setFieldValue(field, api[field], false));
                        });
                    }
                }, []);

                return (
                    <Form>
                        <h1>{isAddMode ? 'Api 추가' : 'Api 편집'}</h1>
                        <div className="form-row">
                            <div className="form-group col">
                                <label>api 이름</label>
                                <Field name="api_name" type="text" className={'form-control' + (errors.api_name && touched.api_name ? ' is-invalid' : '')} />
                                <ErrorMessage name="api_name" component="div" className="invalid-feedback" />
                            </div>
                        </div>
                        <div className="form-row">
                            <div className="form-group col">
                                <label>api 설명</label>
                                <Field name="api_desc" type="text" className={'form-control' + (errors.api_desc && touched.api_desc ? ' is-invalid' : '')} />
                                <ErrorMessage name="api_desc" component="div" className="invalid-feedback" />
                            </div>
                        </div>
                        <div className="form-row">
                            <div className="form-group col-5">
                                <label>api key</label>
                                <Field name="api_key" type="text" className={'form-control' + (errors.api_key && touched.api_key ? ' is-invalid' : '')} />
                                <ErrorMessage name="api_key" component="div" className="invalid-feedback" />
                            </div>
                            <div className="form-group col-5">
                                <label>api endpoint</label>
                                <Field name="api_endpoint" type="text" className={'form-control' + (errors.api_endpoint && touched.api_endpoint ? ' is-invalid' : '')} />
                                <ErrorMessage name="api_endpoint" component="div" className="invalid-feedback" />
                            </div>
                            <div className="form-group col">
                                <label>api data format</label>
                                <Field name="api_data_format" type="text" className={'form-control' + (errors.api_data_format && touched.api_data_format ? ' is-invalid' : '')} />
                                <ErrorMessage name="api_data_format" component="div" className="invalid-feedback" />
                            </div>
                        </div>
                        <div className="form-group">
                            <button type="submit" disabled={isSubmitting} className="btn btn-primary">
                                {isSubmitting && <span className="spinner-border spinner-border-sm mr-1"></span>}
                                Save
                            </button>
                            <Link to={isAddMode ? '.' : '..'} className="btn btn-link">Cancel</Link>
                        </div>
                    </Form>
                );
            }}
        </Formik>
    );
}

export { AddEdit };