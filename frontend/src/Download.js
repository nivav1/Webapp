import React, { useState } from 'react';
import './Download.css';

export default function Download() {
    const [videoUrl, setVideoUrl] = useState('');
    const [isDownloading, setIsDownloading] = useState(false);

    const handleInputChange = (e) => {
        setVideoUrl(e.target.value);
    };

    const downloadVideo = async () => {
        if (!videoUrl.trim()) {
            alert("Please enter a YouTube video URL.");
            return;
        }

        setIsDownloading(true);

        try {
            const response = await fetch(`http://localhost:5000/yt/download`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ youtube_get: videoUrl }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const contentDisposition = response.headers.get('Content-Disposition');
                let filename = 'video.mp4';

                if (contentDisposition) {
                    const filenameMatch = contentDisposition.split('filename=')[1];
                    if (filenameMatch) {
                        filename = filenameMatch.replace(/"/g, '');
                    }
                }
                const url = window.URL.createObjectURL(blob);

                const a = document.createElement("a");
                a.style.display = "none";
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
            }
        } catch (error) {
            alert(`Something went wrong: ${error.message}`);
        } finally {
            setIsDownloading(false);
        }
    };

    return (
        <div className="container">
            <h1>Download YouTube Video</h1>
            <input
                type="text"
                placeholder="Enter YouTube video URL"
                value={videoUrl}
                onChange={handleInputChange}
                className="input-field"
            />
            <br />
            <button
                 onClick={downloadVideo}
                 className={`download-button ${isDownloading ? 'downloading' : ''}`}
                 disabled={isDownloading}
             >
                {isDownloading ? 'Video Downloading...' : 'Download'}
            </button>
        </div>
    );
}
