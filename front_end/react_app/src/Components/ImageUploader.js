import React, { Component } from 'react';
import PropTypes from 'prop-types'
import CanvasCompress from 'canvas-compress';

import { Circle } from 'rc-progress';
import Dropzone from 'react-dropzone';

const darkBlue = '#4788c7'
const lightBlue = '#98ccfd'

const STATUS_IDLE = 'STATUS_IDLE'
const STATUS_COMPRESSING = 'STATUS_COMPRESSING'
const STATUS_UPLOADING = 'STATUS_UPLOADING'

var iconAddImage
//src: https://www.onlinewebfonts.com/icon/245305
//conversion: https://svg2jsx.herokuapp.com/
iconAddImage = (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
    <path d="M929.7,735.2c8.9-16,16.6-32.6,23.8-49.8C977.8,626.7,990,564.2,990,500c0-270-219.7-489.7-489.7-489.7C230.2,10.3,10,230,10,500c0,270,219.7,489.7,489.7,489.7c26.6,0,52.6-2.2,78.6-6.1c55.3-8.9,107.9-27.1,156.6-53.7c25.5,31.5,64.2,52,107.9,52c76.4,0,138.3-62,138.3-138.3C981.1,799.4,961.2,760.1,929.7,735.2z M725.5,915.6c-46.5,25.5-96.8,42.6-149.4,50.9c-24.9,3.9-50.4,6.1-75.8,6.1c-260.6,0-473.1-212.5-473.1-473.1c0-260.6,212.5-473.1,473.1-473.1c260.6,0,473.1,212.5,473.1,473.1c0,62-11.6,122.3-34.9,179.3c-6.6,15.5-13.8,31-22.1,46.5c-21-13.3-45.9-20.5-73-20.5c-76.4,0-138.3,62-138.3,138.3C704.5,869.6,712.2,894.5,725.5,915.6z M941.9,857.5h-78v87.4h-40.9v-87.4h-79.1v-38.2h78.6v-78.6h40.9v78.6h78.6V857.5z"/>
    <path d="M623.1,382.1c0,73-55.3,132.8-122.8,132.8c-68.1,0-122.8-59.2-122.8-132.8c0-73,55.3-132.8,122.8-132.8C567.8,249.9,623.1,309.1,623.1,382.1L623.1,382.1L623.1,382.1z M591,496.1c-22.7,26.6-54.8,38.7-90.8,38.7c-36,0-68.6-12.2-90.8-38.7c-86.9,36-148.3,121.2-148.3,221.3c0,2.8,0,5.5,0,7.7h478.1c0-2.8,0-5.5,0-7.7C739.3,617.9,677.9,532.1,591,496.1L591,496.1z"/>
  </svg>
)

//src: https://www.shareicon.net/uploading-avatar-user-upload-people-up-arrow-user-avatar-700706
/*
iconAddImage_ = (
  <svg id="Capa_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 612">
    <path d="M270.853,310.198c86.177-0.005,117.184-86.291,125.301-157.169C406.154,65.715,364.864,0,270.853,0 c-93.997,0-135.308,65.71-125.301,153.029C153.677,223.907,184.675,310.204,270.853,310.198z"
    />
    <path d="M459.287,346.115c2.773,0,5.528,0.083,8.264,0.235c-4.101-5.85-8.848-11.01-14.403-15.158 c-16.559-12.359-38.005-16.414-56.964-23.864c-9.227-3.625-17.493-7.226-25.253-11.326c-26.184,28.715-60.328,43.736-100.09,43.74 c-39.749,0-73.89-15.021-100.072-43.74c-7.76,4.101-16.026,7.701-25.253,11.326c-18.959,7.451-40.404,11.505-56.964,23.864 c-28.638,21.375-36.039,69.46-41.854,102.26c-4.799,27.076-8.023,54.707-8.965,82.209c-0.729,21.303,9.79,24.29,27.611,30.721 c22.315,8.048,45.358,14.023,68.552,18.921c44.797,9.46,90.973,16.729,136.95,17.054c22.277-0.159,44.601-1.956,66.792-4.833 c-16.431-23.807-26.068-52.645-26.068-83.695C311.575,412.378,377.839,346.115,459.287,346.115z"
    />
    <path d="M456.128,375.658c-65.262,0-118.172,52.909-118.172,118.171S390.865,612,456.128,612 c65.262,0,118.172-52.909,118.172-118.171C574.299,428.567,521.39,375.658,456.128,375.658z M504.765,483.703 c-3.234,3.233-7.471,4.849-11.71,4.849c-4.237,0-8.476-1.616-11.71-4.851l-8.655-8.655v77.546c0,9.146-7.414,16.559-16.559,16.559 s-16.559-7.414-16.559-16.559v-77.55l-8.662,8.662c-6.467,6.465-16.952,6.467-23.419-0.002c-6.467-6.467-6.467-16.952,0-23.419 l36.931-36.926c6.467-6.465,16.952-6.467,23.419,0l36.925,36.926C511.232,466.751,511.232,477.236,504.765,483.703z"
    />
</svg>
)
*/

const iconCancelButton = (width) => {
  return(
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width={width} height={width}>
      <g id="surface1">
          <path d="M 20 38.5 C 9.800781 38.5 1.5 30.199219 1.5 20 C 1.5 9.800781 9.800781 1.5 20 1.5 C 30.199219 1.5 38.5 9.800781 38.5 20 C 38.5 30.199219 30.199219 38.5 20 38.5 Z"
          fill="#98ccfd" />
          <path d="M 20 2 C 29.925781 2 38 10.074219 38 20 C 38 29.925781 29.925781 38 20 38 C 10.074219 38 2 29.925781 2 20 C 2 10.074219 10.074219 2 20 2 M 20 1 C 9.507813 1 1 9.507813 1 20 C 1 30.492188 9.507813 39 20 39 C 30.492188 39 39 30.492188 39 20 C 39 9.507813 30.492188 1 20 1 Z"
          fill="#4788c7" />
          <path d="M 13.988281 28.132813 L 11.867188 26.011719 L 26.011719 11.867188 L 28.132813 13.988281 Z"
          fill="#fff" />
          <path d="M 11.867188 13.988281 L 13.988281 11.867188 L 28.132813 26.011719 L 26.011719 28.132813 Z"
          fill="#fff" />
          <path d="M 28.132813 13.988281 L 26.011719 11.867188 L 20 17.878906 L 13.988281 11.867188 L 11.867188 13.988281 L 17.878906 20 L 11.867188 26.011719 L 13.988281 28.132813 L 20 22.121094 L 26.011719 28.132813 L 28.132813 26.011719 L 22.121094 20 Z"
          fill="#fff" />
      </g>
  </svg>
  )
}

const styleCancelButton = {
  position: 'absolute',
  top:'50%',
  left:'50%',
  transform: 'translate(-50%, -50%)'
}

class ImageUploader extends Component{

  constructor(props, context){
    super(props, context);
    this.abortUpload = this.abortUpload.bind(this)
    this.onSuccess = this.onSuccess.bind(this)
    this.onError = this.onError.bind(this)
    this.onSelectFiles = this.onSelectFiles.bind(this)
    //Initialize the states
    this.state = {
      status: STATUS_IDLE,
      compressionProgress: undefined,
      uploadProgress: undefined,
      rawFiles: [],
      compressedFiles: []
    }
    const width = '' + Math.round(this.props.width / 2)
    //src: https://icons8.com/icon/set/cancel/all
    this.iconCancelButton = iconCancelButton(width)
  }

  //src: https://icons8.com/icon/set/cancellation/all

  /**
  * Uploads the files to an endpoint determined by the props
  * @param: an array of file objects
  */
  uploadFiles = (files) => {
    var formData = new FormData();
    files.forEach(
      (file, index) => {formData.append(index +'_'+ file.name, file)}
    )
    var xhr = new XMLHttpRequest();
    // progress callback is called frequently by the xhr handler during the upload
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable){
        var percent = Math.round(100 * event.loaded / event.total);
        this.onProgress(percent)
      }
    };
    // when uplaod is finished successfully
    xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE){
          if( xhr.status >= 200 && xhr.status < 300) {
            this.onSuccess(xhr.responseText)
          } else {
            this.onError()
          }
        }
      }
    // callback to handle errors
    xhr.upload.onerror = event => {
      this.onError()
    };
    // open the xhr and disable the browser caching
    xhr.open('POST', this.props.endpoint);
    xhr.setRequestHeader('Cache-Control', 'no-cache');
    xhr.send(formData);
    return () => {
      xhr.upload.onprogress = null;
      xhr.upload.onerror = null;
      xhr.upload.onabort = null;
      xhr.onreadystatechange = null;
      xhr.abort();
      this.onAbortUpload();
      // set abort upload to an empty function
    }
  }

  /**
  * Compress Image files
  */
  compressImages(files){
    const compressor = new CanvasCompress({
        type: CanvasCompress.MIME.JPEG,
        width: this.props.maxWidthHeight,
        height: this.props.maxWidthHeight,
        quality: this.props.compressionRatio,
    });
    files.forEach(
      file => compressor.process(file).then(({ source, result }) => {
        // const { blob, width, height } = source;
        // const { blob, width, height } = result;
        const { blob } = result;
        this.addToCompressedFiles(blob)
    }));
  }

  onAbortUpload() {
    this.setState({
      status: STATUS_IDLE,
    })
    this.abortUpload = () => {}
  }

  onProgress(percent){
    this.setState({
      uploadProgress: percent,
    })
  }

  onSuccess(responseText){
    this.setState({
      status: STATUS_IDLE
    })
    if (this.props.onSuccess){
      this.props.onSuccess.call(this, responseText)
    }
  }

  onError(){
    this.setState({
      status: STATUS_IDLE
    })
    if (this.props.onError){
      this.props.onError.call(this)
    }
  }

  onSelectFiles(files){
    this.setState({
      status: STATUS_COMPRESSING,
      compressionProgress: 0,
      rawFiles: files,
      compressedFiles: [],
    })
    // Call the upload files and set the callback for upload abortion
    this.compressImages(files)
    // run the refrenced onSelectFiles
    if (this.props.onSelectFiles){
      this.props.onSelectFiles.call(this, files)
    }
  }

  /**
  * After compressing each file, this method is called
  */
  addToCompressedFiles(file){
    this.setState({
      compressedFiles: [ ...this.state.compressedFiles, file],
    })
    if (this.state.rawFiles.length === this.state.compressedFiles.length){
      this.setState({
        status: STATUS_UPLOADING,
        uploadProgress: 0,
      })
      this.abortUpload = this.uploadFiles(this.state.compressedFiles);
    } else {
      const percent = Math.round(100 * this.state.compressedFiles.length / this.state.rawFiles.length)
      this.setState({
        compressionProgress: percent
      })
    }
  }

  abortUpload(){
    // Empty function
    // This function gets assigned as return value of this.uploadFiles(...)
  }

  render(){
    var dropzoneContain = null
    if (this.state.status === STATUS_UPLOADING){
      dropzoneContain = (
        <div style={{position:'relative'}}>
          <Circle
            percent={this.state.uploadProgress}
            trailColor= { darkBlue }
            trailWidth="1.5"
            strokeWidth="6"
            strokeColor= { lightBlue } />
          <div
            style={ styleCancelButton }
            onClick={(e)=>{
              e.stopPropagation()
              this.abortUpload()
            }}>
            { this.iconCancelButton }
          </div>
        </div>
      )
    } else if (this.state.status === STATUS_COMPRESSING) {
      dropzoneContain =  (
        <Circle
          percent={this.state.compressionProgress}
          trailColor= { darkBlue }
          trailWidth="1.5"
          strokeWidth="6"
          strokeColor={ darkBlue } />
      )
    } else {
      dropzoneContain = (
        <div style={{fill: darkBlue}}>
        { iconAddImage }
        </div>
      )
    }

    //         fill="#4788c7"  #98ccfd
    return(
      <div style={ {width: this.props.width} }>
      <Dropzone
        onDrop={ (files) => {this.onSelectFiles(files)} }
        style={{}}
        accept= { 'image/*' }
        disabled = {this.state.status !== STATUS_IDLE}>
        { dropzoneContain }
      </Dropzone>
      </div>
    )
  }
}

export default ImageUploader;

ImageUploader.propTypes = {
  /**
  * The url destination for the files to be uploaded to
  */
  endpoint: PropTypes.string,

  /**
  * width and heigh of the compressed file
  */
  maxWidthHeight: PropTypes.number,
  /**
  * width (and heigh) of the componenet on the DOM
  */
  width: PropTypes.number,
  /**
  * A number between 0 .. 1
  * 0: low quality and hight compression; 1: no compression
  */
  compressionRatio: PropTypes.number,

  /**
  * Called if the upload is successful
  */
  onSuccess: PropTypes.func,
  /**
  * Called if there is an error in upload
  */
  onError: PropTypes.func,
  /**
  * Called when the files are selected
  */
  onSelectFiles: PropTypes.func,
}

ImageUploader.defaultProps = {
  endpoint: '/uploads',
  width: 200,
  maxWidthHeight: 750,
  compressionRatio: 0.9,
  onSuccess: null,
  onError: null,
  onSelectFiles: null,
}
