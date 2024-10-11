import React from 'react';
import { Heart, ThumbsDown } from 'lucide-react';
import { Button } from "@/components/ui/button";

const ImageGrid = ({ images, onImageClick }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {images.map((image) => (
        <div
          key={image.id}
          className="relative group"
        >
          <div className="absolute top-2 right-2 flex space-x-2 z-10">
            <Button size="sm" variant="ghost" className="bg-transparent hover:bg-transparent">
              <Heart className="h-4 w-4 text-white" />
            </Button>
            <Button size="sm" variant="ghost" className="bg-transparent hover:bg-transparent">
              <ThumbsDown className="h-4 w-4 text-white" />
            </Button>
          </div>
          <div className="aspect-[426/240] overflow-hidden rounded-lg">
            <img
              src={image.url}
              alt={image.code}
              className="w-full h-full object-cover cursor-pointer"
              onClick={() => onImageClick(image)}
            />
          </div>
          <div className="mt-2 text-center">
            <p className="text-sm">{image.code}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImageGrid;