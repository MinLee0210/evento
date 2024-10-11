import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

const ImageModal = ({ image, onClose, onSearchSimilar }) => {
  if (!image) return null;

  return (
    <Dialog open={!!image} onOpenChange={onClose}>
      <DialogContent className="w-11/12 max-w-[1600px] h-[90vh] max-h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>{image.code}</DialogTitle>
          <DialogDescription>
            Details about the related video
          </DialogDescription>
        </DialogHeader>
        <div className="flex-grow flex flex-col overflow-auto">
          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Image Details</h3>
            <p>Additional information about the image and related video would go here.</p>
          </div>
          <div className="w-full max-w-[980px] mx-auto mb-4">
            <div className="aspect-[980/552]">
              <img src={image.url} alt={image.code} className="w-full h-full object-cover rounded-lg" />
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Related Video Information</h3>
            <p>More details about the video, such as duration, upload date, views, etc., can be displayed here.</p>
          </div>
        </div>
        <div className="mt-4 w-full">
          <Button onClick={onSearchSimilar} className="w-full py-6 text-lg">Search Similar Images</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default ImageModal;