import React, { useState, useRef, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Mic, Image as ImageIcon, Search as SearchIcon, X } from 'lucide-react';
import { ReactPlayer } from 'react-player';
import axios from 'axios';

import { fetchSearchResults } from '../api/search';
const Search = () => {
  const [query, setQuery] = useState('');
  const [kNeighbors, setKNeighbors] = useState(50); // Default 50
  const [strength, setStrength] = useState(1); // Default 1
  const [searchResults, setSearchResults] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [shouldShowReload, setShouldShowReload] = useState(false); // For "Load Again" button

  const handleSearch = async () => {
    try {
      const query_info = {
        query: query,
        top_k: kNeighbors,
      };
  
      const response = await axios.post(BACKEND_URL_SEARCH, JSON.stringify(query_info));
  
      if (response.status === 200) {
        const data = response.data;
  
        // Critical validation!  Check if the structure is as expected
        if (
          data &&
          Array.isArray(data.scores) &&
          Array.isArray(data.idx_image) &&
          Array.isArray(data.infos_query) && 
          Array.isArray(data.vid_urls) && 
          Array.isArray(data.embed_urls) && 
          Array.isArray(data.frames) && 
          data.scores[0].length === data.idx_image.length &&
          data.scores[0].length === data.infos_query.length &&
          data.scores[0].length === data.vid_urls.length &&
          data.scores[0].length === data.embed_urls.length &&
          data.scores[0].length === data.frames.length
        ) {
          const results = data.idx_image.map((path, index) => ({
            path,
            score: data.scores[0][index], // Extract the score at the correct index
            id: data.idx_image[index], 
            thumbnail_id: data.infos_query[index], 
            vid_url: data.vid_urls[index], 
            embed_url: data.embed_urls[index], 
            frame: data.frames[index], 
          }));
          setSearchResults(results);
        } else {
          console.error("Invalid response structure from the server.");
          setSearchResults([]); // Important: Handle unexpected data.
        }
      } else {
        console.error("Error fetching search results:", response.status, response.data);
        setSearchResults([]); // Important: Set to empty array on server error
      }
    } catch (error) {
      console.error("Error fetching search results:", error);
      setSearchResults([]); // Handle any other error.
    }
  };

  const handleReload = () => {
    handleSearch(); 
    setShouldShowReload(false);
  };

  
  useEffect(() => {
   
    if (kNeighbors !== 50 || strength !== 1) {
      setShouldShowReload(true);
    } else {
      setShouldShowReload(false);
    }
  }, [kNeighbors, strength]);

  return (
    <div className="px-4 py-8">
      <h1 className="mb-8 text-3xl font-bold text-center">Image and Video Retrieval</h1>
      
      <div className="flex items-center mb-8">
        <Input
          type="text"
          placeholder="Enter your search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow mr-2"
        />
        <Button variant="outline" className="mr-2">
          <Mic className="w-4 h-4" />
        </Button>
        <Button variant="outline" className="mr-2">
          <ImageIcon className="w-4 h-4" />
        </Button>
        <Button onClick={handleSearch}>
          <SearchIcon className="w-4 h-4 mr-2" />
          Search
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-8 mb-8 md:grid-cols-2">
        <div>
          <label className="block mb-2 text-sm font-medium">K-Neighbors: {kNeighbors}</label>
          <Slider
            min={1}
            max={200}
            step={1}
            value={[kNeighbors]}
            onValueChange={(value) => setKNeighbors(value[0])}
          />
        </div>
        <div>
          <label className="block mb-2 text-sm font-medium">Strength: {strength}</label>
          <Slider
            min={1}
            max={10}
            step={1}
            value={[strength]}
            onValueChange={(value) => setStrength(value[0])}
          />
        </div>
      </div>

      {shouldShowReload && (
        <Button className="mb-4" onClick={handleReload}>
          Load Again
        </Button>
      )}

      <MediaGrid items={searchResults} onItemClick={setSelectedItem} />

      {selectedItem && (
        <MediaModal
          item={selectedItem}
          onClose={() => setSelectedItem(null)}
          onSearchSimilar={() => {
            console.log('Search similar items for:', selectedItem.code);
          }}
        />
      )}
    </div>
  );
};

const MediaGrid = ({ items, onItemClick }) => {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {items.map((item) => (
        <MediaItem key={item.id} item={item} onClick={() => onItemClick(item)} />
      ))}
    </div>
  );
};

const MediaItem = ({ item, onClick }) => {
  const videoRef = useRef(null);

  const handleMouseEnter = () => {
    if (item.type === 'video' && videoRef.current) {
      videoRef.current.play();
    }
  };

  const handleMouseLeave = () => {
    if (item.type === 'video' && videoRef.current) {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
  };

  return (
    <div 
      className="relative transition-shadow duration-300 ease-in-out cursor-pointer aspect-video hover:shadow-lg"
      onClick={onClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {
      <img src={`${BACKEND_URL_GET_IMAGE}/${item.thumbnail_id}`} alt={item.id} className="object-cover w-full h-full" />
      }


      <div className="absolute bottom-0 left-0 right-0 p-2 text-sm text-white bg-black bg-opacity-50">
        {item.id}
      </div>
    </div>
  );
};

const MediaModal = ({ item, onClose, onSearchSimilar }) => {
  const modalRef = useRef(null);

  const handleBackdropClick = (e) => {
    if (modalRef.current && !modalRef.current.contains(e.target)) {
      onClose(); 
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75"
      onClick={handleBackdropClick} 
    >
      <div 
        ref={modalRef} 
        className="relative max-w-4xl p-8 bg-white"
      >
        <button 
          className="absolute text-red-600 top-2 right-2"
          onClick={onClose}
        >
          <X className="w-6 h-6" />
        </button>
        <div className="mb-4 aspect-video">
          {item.type === 'image' ? (
            <img src={item.thumbnail_id} alt={item.code} className="object-contain w-full h-full" />
          ) : (
            // <video 
            // src={item.vid_url} 
            // controls 
            // className="w-full h-full" />
            <a href={item.vid_url} 
            target="_blank" 
            rel="noopener noreferrer">
              <iframe
              id="displayFrame"
              src={item.embed_url} 
              controls 
              className="w-full h-full"
              frameborder="1"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            />
            </a>
          )}
        </div>
        <p className="mb-4 text-lg font-semibold">Keyframe: {item.frame}</p>
        <p className='text-lg font-semibold'>Title Video or IMG</p>
        <p className='mt-4 mb-10 text-sm font-semibold text-slate-700'>Description</p>
        <Button onClick={onSearchSimilar}>Search Similar</Button>
      </div>
    </div>
  );
};

export default Search;
