import FileUploader from './ImageUploader'
import React from 'react'

import Loading from 'react-loading-components'
import { iconPuppyFace } from '../icons'

/* Ready to accept a photo */
const STATUS_BEGIN = 'STATUS_BEGIN'
/* Ready to accept a photo */
const STATUS_IMAGE_SELECTED = 'STATUS_IMAGE_SELECTED'
/* REquesting the server the type of puppy and other things */
const STATUS_POLLING_PUPPY = 'STATUS_POLLING_PUPPY'
/* when the results are read from the servers */
const STATUS_PUPPY_RESULT_BACK = 'STATUS_PUPPY_RESULT_BACK'
/**/
const RESPONSE_WAIT = 'WAIT'

const HOST_URL = '' // 'http://0.0.0.0:5001'

class App extends React.Component{
  constructor(props){
    super(props)
    this.pollServer = this.pollServer.bind(this)
    this.state = {
      images: [],
      dogImages: [],
      status: STATUS_BEGIN,
      breed: undefined,
      nrof_faces: undefined
    }
  }

  /**
  * Keeps polling the server for the name of puppy
  */
  inquirePuppy(){
    this.setState({
      status: STATUS_POLLING_PUPPY,
      breed: undefined,
      dogImages: [],
      nrof_faces: undefined
    })
    this.pollServer()
  }

  /**
  * Poll the server for the resutls on images
  * the FormData includes id's of images
  */
  pollServer(){
    var formData = new FormData()
    this.state.images.forEach( (image, index) => {
      formData.append(index, image)
    })
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200){
        //console.log('response: ', xhr.responseText)
        const respObj = JSON.parse(xhr.responseText)
        this.onPuppyResultBack(respObj) // changes the status if satisfied with results
        if (this.state.status === STATUS_POLLING_PUPPY){
          setTimeout(this.pollServer, 1000);
        }
      }
    }
    xhr.open('POST', HOST_URL + '/puppier')
    xhr.setRequestHeader('Cache-Control', 'no-cache');
    xhr.send(formData)
  }

  /**
  * is called when the response from the server is received and
  * the type of 'puppy' is known
  * This function is called on two occasions:
  *  1. The breed is determined
  *  2. The nrof_faces is determined
  */
  onPuppyResultBack(respObj){
    var dogImages = []
    if (respObj.breed !== undefined){
      const breed = respObj.breed
      Object.keys(respObj).forEach(key => {
        if (key === 'dog_images' && respObj.dog_images !== undefined){
          dogImages = [ ...respObj.dog_images]
        }
      })
      this.setState({
        status: STATUS_PUPPY_RESULT_BACK,
        breed,
        dogImages,
      })
    }
    if (this.state.nrof_faces === undefined && respObj.nrof_faces !== undefined){
      this.setState({
        nrof_faces: respObj.nrof_faces,
      })
    }
  }

  startOver(){
    this.setState({
      status: STATUS_BEGIN,
      images: [],
      breed: undefined,
      nrof_faces: undefined
    })
  }

  didImageUpload(response){
    this.setState({
      status: STATUS_IMAGE_SELECTED,
      images: JSON.parse(response),
    })
  }

  render(){
    var btnPuppy
    if (this.state.status === STATUS_POLLING_PUPPY){
      btnPuppy = <Loading type='grid' fill='#000' />
    } else {
      btnPuppy = <div> { iconPuppyFace } <br></br> <span> Puppy Me! </span> </div>
    }
    const images = this.state.images.map((image, index) => (
                    <img
                     key = {index}
                     className="img-responsive img-thumbnail"
                     style= {{maxWidth: "90%"}}
                     src={HOST_URL + '/bank/' + image}
                     alt=''></img>
                   ))
    const dogImages = (
      <div>
        {this.state.dogImages.map((image, index) => (
            <img
              key = { index }
              className="img-responsive img-thumbnail"
              style= {{maxWidth: "70%"}}
              src={HOST_URL + '/dog_images/' + image}
            />
        ))}
      </div>
    )
    const btnStartOver = (
      <button type="button" className="btn btn-success btn-lg"
        onClick={() => this.startOver()}
        >Start over</button>
    )
    const nrof_human_faces =(
      (this.state.nrof_faces === undefined) ? '' : (
        <div className="alert alert-info" role="alert">
          We recognized { this.state.nrof_faces } human face(s) in the photo.
        </div>
      ))
    var content
    switch (this.state.status){
      case STATUS_BEGIN:
        content = (
          <div>
            <div className="alert alert-info" role="alert">
              Start by choosing a photo of yourself or your dog below
            </div>
            <FileUploader width={175} endpoint = {HOST_URL + '/upload'}
              onSuccess = {response => this.didImageUpload(response)}/>
          </div>
        )
        break
      case STATUS_IMAGE_SELECTED:
      case STATUS_POLLING_PUPPY:
        content = (
          <div>
            { images }
            <br></br><br></br>
            { nrof_human_faces }
            <button type="button" className="btn btn-default btn-lg"
              onClick={()=>this.inquirePuppy()}>
                  { btnPuppy }
            </button>
            <br></br><br></br>
            { btnStartOver }
          </div>
        )
        break
      case STATUS_PUPPY_RESULT_BACK:
        content = (
          <div>
            { images }
            <br></br><br></br>
            { nrof_human_faces }
            <div className="alert alert-info" role="alert">
              We think this photo resembles the
              <h4> {this.state.breed} </h4>
              breed.
            </div>
            { btnStartOver }
            <br></br><br></br>
            { dogImages }
          </div>
        )
        break
      default:
        console.log('Unhandled status')
    }
    return(
      <div className="container">
        <center>
          <div className="row">
              <div className="col-sm-12">
                { content }
              </div>
          </div>
        </center>
      </div>
    )
  }
}


export default App
