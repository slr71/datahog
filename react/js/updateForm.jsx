import React from 'react';
import axios from 'axios';
import { LabeledInput } from './util';

export class IrodsForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: this.props.lastAttempt.username,
            password: '',
            host: this.props.lastAttempt.irods_host,
            port: this.props.lastAttempt.irods_port,
            zone: this.props.lastAttempt.irods_zone,
            folder: this.props.lastAttempt.top_folder,
            waiting: false,
            failed: false,
            error: ''
        };

        this.handleChange = this.handleChange.bind(this);
        this.submitForm = this.submitForm.bind(this);
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    submitForm(event) {
        event.preventDefault();
        this.setState({
            waiting: true,
            error: ''
        });
        axios.post('/api/import/irodslogin', {
            user: this.state.user,
            password: this.state.password,
            host: this.state.host,
            port: this.state.port,
            zone: this.state.zone,
            folder: this.state.folder
        })
        .then(function(response) {
            this.setState({
                waiting: false
            });
            this.props.updateTriggered();
        }.bind(this))
        .catch(function(error) {
            this.setState({
                waiting: false,
                error: error.response.data
            });
        }.bind(this));
    }
    
    render() {
        let submitDisabled = (
            this.state.waiting || 
            !this.state.user.length || 
            !this.state.password.length || 
            !this.state.host.length || 
            !this.state.folder.length || 
            !this.state.port.length || 
            !this.state.zone.length
        );
        return (
            <div className="column col-9 col-mx-auto">
                <form className="card" onSubmit={this.submitForm}>
                    <div className="card-header">
                        <div className="card-title h5">Import from iRODS</div>
                    </div>
                    <div className="card-body form-horizontal">
                        <div className="form-group">
                            <div className="col-2">
                                <br/>
                                <label>Server</label>
                            </div>
                            <div className="col-4">
                                <LabeledInput name="host"
                                    label="Host"
                                    value={this.state.host}
                                    onChange={this.handleChange}/>
                            </div>
                            <div className="col-2">
                                <LabeledInput name="port"
                                    label="Port"
                                    value={this.state.port}
                                    onChange={this.handleChange}/>
                            </div>
                            <div className="col-4">
                                <LabeledInput name="zone"
                                    label="Zone"
                                    value={this.state.zone}
                                    onChange={this.handleChange}/>
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-3">
                                <br/>
                                <label>Credentials</label>
                            </div>
                            <div className="col-4">
                                <LabeledInput name="user"
                                    label="Username"
                                    value={this.state.user}
                                    onChange={this.handleChange}/>
                            </div>
                            <div className="col-4">
                                <LabeledInput type="password"
                                    name="password"
                                    label="Password"
                                    value={this.state.password}
                                    onChange={this.handleChange}/>
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-3">
                                <br/>
                                <label>Folder to Import</label>
                            </div>
                            <div className="col-8">
                                <LabeledInput name="folder"
                                    label="Folder"
                                    value={this.state.folder}
                                    onChange={this.handleChange}/>
                            </div>
                        </div>
                    </div>
                    <div className="card-footer">
                        <input type="submit" 
                            className="btn btn-primary"
                            value="Import from iRODS"
                            disabled={submitDisabled} />
                        <div className="float-right text-right">
                            { this.state.waiting ?
                                <span className="text-primary">
                                    <i className="loading">load</i> Connecting to iRODS...
                                </span> :
                                <span className="text-error">
                                    {this.state.error}
                                </span>
                            }
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}



export class CyverseForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: this.props.lastAttempt.username,
            password: '',
            folder: this.props.lastAttempt.top_folder,
            waiting: false,
            failed: false,
            error: ''
        };

        this.handleChange = this.handleChange.bind(this);
        this.submitForm = this.submitForm.bind(this);
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    submitForm(event) {
        event.preventDefault();
        this.setState({
            waiting: true,
            error: ''
        });
        axios.post('/api/import/cyverselogin', {
            user: this.state.user,
            password: this.state.password,
            folder: this.state.folder
        })
        .then(function(response) {
            this.setState({
                waiting: false
            });
            this.props.updateTriggered();
        }.bind(this))
        .catch(function(error) {
            this.setState({
                waiting: false,
                error: error.response.data
            });
        }.bind(this));
    }
    
    render() {
        let submitDisabled = (
            this.state.waiting || 
            !this.state.user.length || 
            !this.state.password.length ||
            !this.state.folder.length
        );
        return (
            <div className="column col-9 col-mx-auto">
                <form className="card" onSubmit={this.submitForm}>
                    <div className="card-header">
                        <div className="card-title h5">Import from CyVerse</div>
                    </div>
                    <div className="card-body form-horizontal">
                        <div className="form-group">
                            <div className="col-3">
                                <br/>
                                <label>Credentials</label>
                            </div>
                            <div className="col-4">
                                <LabeledInput name="user"
                                    label="Username"
                                    value={this.state.user}
                                    onChange={this.handleChange}/>
                            </div>
                            <div className="col-4">
                                <LabeledInput type="password"
                                    name="password"
                                    label="Password"
                                    value={this.state.password}
                                    onChange={this.handleChange}/>
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-3">
                                <br/>
                                <label>Folder to Import</label>
                            </div>
                            <div className="col-8">
                                <LabeledInput name="folder"
                                    label="Folder"
                                    value={this.state.folder}
                                    onChange={this.handleChange}/>
                            </div>
                        </div>
                    </div>
                    <div className="card-footer">
                        <input type="submit" 
                            className="btn btn-primary"
                            value="Import from iRODS"
                            disabled={submitDisabled} />
                        <div className="float-right text-right">
                            { this.state.waiting ?
                                <span className="text-primary">
                                    <i className="loading">load</i> Connecting to CyVerse...
                                </span> :
                                <span className="text-error">
                                    {this.state.error}
                                </span>
                            }
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}