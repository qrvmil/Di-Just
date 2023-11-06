// import axios from 'axios';
// const API_URL = 'http://localhost:8000';


// function getToken() {
//     const tokenString = localStorage.getItem('token');
//     const userToken = JSON.parse(tokenString);
//     return userToken?.token
// }

// function getUserId() {
//     const userStringId = localStorage.getItem('token')
//     const userId = JSON.parse(userStringId);
//     return userId.user;
// }




// export default class Service{
	
// 	constructor(){}

    
    
//     // user + profile
    
//     getAllProfiles() {
//         const url = `${API_URL}/users/profiles/`;
//         return axios.get(url).then(response => response.data);
//     }
    
    
//     // updateInfo - formData/object
//     profileUpdate(updateInfo) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.put(`${API_URL}/users/update/${getUserId()}/`, updateInfo, {headers: {"Authorization" : "Token " + token}})
//                 .then(res => {
//                     res.data})
//     }
    
//     profilePictureUpdate(picture) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.put(`${API_URL}/users/profile/update/picture/${getUserId()}/`, {
//             picture: picture,
//             }, {headers: {"Authorization" : "Token " + TOKEN, "Content-Type": "multipart/form-data"}})
//             .then(res => { res.data })
//     }
    
//     updatePassword(password) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.put(`${API_URL}/users/profile/update/password/${getUserId()}/`, {password: password}, 
//         {headers: {"Authorization" : "Token " + TOKEN}}).then(
//             res => { res.data })
//     }

//     followUser(id) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.post(`${API_URL}/users/follow/${id}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     unfollowUser(id) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.post(`${API_URL}/users/unfollow/${id}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
    
//     }
    
//     getSavedImgDigests () {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.put(`${API_URL}/users/saved-img-digests/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data);
//     }
    
//     getSavedLinkDigests() {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.put(`${API_URL}/users/saved-link-digests/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data);
//     }
    
    
//     // Image Digest activity
    
    
//     // formData == formData object
//     createImageDigest(formData)
//      {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.post(`http://127.0.0.1:8000/img-digest/create/`, formData, {headers: {"Authorization" : "Token " + token, 'Content-Type': 'multipart/form-data'}})
//                 .then(res => res.data)
//      }
    
//     updateImageDigest() {
    
//      }
    
//     getImageDigest(id) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.get(`${API_URL}/img-digest/get/${id}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     deleteImageDigest (id) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.get(`${API_URL}/img-digest/delete/${id}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     createdImgDigests (uid) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.get(`${API_URL}/img-digest/user/${uid}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     // info == Object
//     listOfImgDigests (info) {
//         const keys = Object.keys(info);
       
//         axios.get(`${API_URL}/img-all/`, info).then(res => res.data)
        
//     }
    
    
//     // Link digest activity
    
//     // formData == formData object
//     createLinkDigest(formData) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.post(`http://127.0.0.1:8000/link-digest/create/`, formData, {headers: {"Authorization" : "Token " + token, 'Content-Type': 'multipart/form-data'}})
//                 .then(res => res.data)
//      }
    
//     updateLinkDigest() {
    
//      }
    
//     getLinkDigest(id) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.get(`${API_URL}/link-digest/get/${id}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     deleteLinkDigest (id) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.get(`${API_URL}/link-digest/delete/${id}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     createdLIinkDigests (uid) {
//         const tokenString = localStorage.getItem('token');
//         const userToken = JSON.parse(tokenString);
//         token = userToken?.token;
//         return axios.get(`${API_URL}/link-digest/user/${uid}/`, {headers: {"Authorization" : "Token " + token}}).then(res => res.data)
//     }
    
//     // info == Object
//     listOfLinkDigests (info) {
//         const keys = Object.keys(info);
       
//         axios.get(`${API_URL}/link-all/`, info).then(res => res.data)
        
//     }
    
    
    
	
	
	
// }


