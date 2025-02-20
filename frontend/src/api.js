import axios from "axios";

const API_BASE = "http://localhost:8000";

export const uploadResume = (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return axios.post(`${API_BASE}/upload/`, formData);
};

export const getResumes = () => axios.get(`${API_BASE}/resumes/`);

export const getResumeDetails = (id) => axios.get(`${API_BASE}/resume/${id}`);