import React, { useState } from 'react';
import axios from 'axios';
import { API_URL, TOKEN } from './config';

export default function UploadForm({ onUpload }) {
  const [file, setFile] = useState(null);
  const [name, setName] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please choose a CSV file");

    const form = new FormData();
    form.append("file", file);
    form.append("name", name || file.name);

    try {
      const res = await axios.post(API_URL + "upload/", form, {
        headers: {
          'Authorization': `Token ${TOKEN}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      onUpload(res.data);
    } catch (err) {
      alert("Upload failed: " + err.response?.data?.error);
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <input 
        type="text"
        placeholder="Dataset name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      
      <input 
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button type="submit">Upload CSV</button>
    </form>
  );
}
