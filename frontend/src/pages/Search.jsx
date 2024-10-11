import React, { useState, useRef, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Mic, Image as ImageIcon, Search as SearchIcon, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom'; // Change here

const Search = () => {
  const [query, setQuery] = useState('');
  const [kNeighbors, setKNeighbors] = useState(50); // Default 50
  const [strength, setStrength] = useState(1); // Default 1
  const [searchResults, setSearchResults] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [shouldShowReload, setShouldShowReload] = useState(false); // For "Load Again" button
  const navigate = useNavigate(); // Change here

  const handleSearch = () => {
    
    console.log('Searching with:', { query, kNeighbors, strength });

    setSearchResults(Array(kNeighbors).fill().map((_, i) => ({
      id: i,
      type: i % 3 === 0 ? 'video' : 'image',
      url: i % 3 === 0 
        ? `https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4` 
        : `https://picsum.photos/1600/900?random=${i}`,
      code: `ITEM_${i.toString().padStart(4, '0')}`,
    })));

    
    if (query) {
      router.push(`/search/${query}`);
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
      {item.type === 'image' ? (
        <img src={item.url} alt={item.code} className="object-cover w-full h-full" />
      ) : (
        <video 
          ref={videoRef}
          src={item.url} 
          className="object-cover w-full h-full" 
          loop 
          muted 
          playsInline
        />
      )}
      <div className="absolute bottom-0 left-0 right-0 p-2 text-sm text-white bg-black bg-opacity-50">
        {item.code}
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
            <img src={item.url} alt={item.code} className="object-contain w-full h-full" />
          ) : (
            <video src={item.url} controls className="w-full h-full" />
          )}
        </div>
        <p className="mb-4 text-lg font-semibold">Keyframe: {item.code}</p>
        <p className='text-lg font-semibold'>Title Video or IMG</p>
        <p className='mt-4 mb-10 text-sm font-semibold text-slate-700'>Description</p>
        <Button onClick={onSearchSimilar}>Search Similar</Button>
      </div>
    </div>
  );
};

export default Search;
