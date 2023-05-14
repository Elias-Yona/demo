use project2

db.createCollection("file_uploads", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["file_name", "file_type", "file_size", "upload_date", "uploaded_by", "description", "tags", "file_url"],
      properties: {
        file_name: {
          bsonType: "string",
          description: "The name of the uploaded file."
        },
        file_type: {
          bsonType: "string",
          description: "The type or MIME type of the uploaded file."
        },
        file_size: {
          bsonType: "long",
          description: "The size of the uploaded file in bytes."
        },
        upload_date: {
          bsonType: "date",
          description: "The date and time when the file was uploaded."
        },
        uploaded_by: {
          bsonType: "string",
          description: "The name or ID of the user who uploaded the file."
        },
        description: {
          bsonType: "string",
          description: "A brief description or comment about the file."
        },
        tags: {
          bsonType: "array",
          items: {
            bsonType: "string"
          },
          description: "An array of tags or keywords that describe the contents of the file."
        },
        file_url: {
          bsonType: "string",
          description: "The URL or path to the uploaded file."
        }
      }
    }
  }
})


db.runCommand({
  collMod: "file_uploads",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["file_name", "file_type", "file_size", "upload_date", "uploaded_by", "description", "tags", "file_url", "frame_range", "starttime_code"],
      properties: {
        file_name: {
          bsonType: "string",
          description: "The name of the uploaded file."
        },
        file_type: {
          bsonType: "string",
          description: "The type or MIME type of the uploaded file."
        },
        file_size: {
          bsonType: "long",
          description: "The size of the uploaded file in bytes."
        },
        upload_date: {
          bsonType: "date",
          description: "The date and time when the file was uploaded."
        },
        uploaded_by: {
          bsonType: "string",
          description: "The name or ID of the user who uploaded the file."
        },
        description: {
          bsonType: "string",
          description: "A brief description or comment about the file."
        },
        tags: {
          bsonType: "array",
          items: {
            bsonType: "string"
          },
          description: "An array of tags or keywords that describe the contents of the file."
        },
        file_url: {
          bsonType: "string",
          description: "The URL or path to the uploaded file."
        },
        'frame_range': {
            'bsonType': 'object',
            'required': ['start_timecode', 'num_frames'],
            'properties': {
                'start_timecode': {
                    'bsonType': 'string',
                    'description': 'The start timecode of the range of frames to extract.'
                },
                'num_frames': {
                    'bsonType': 'int',
                    'minimum': 1,
                    'maximum': 1000,
                    'description': 'The number of frames to extract from the video.'
                }
            }
        },
          start_timecode: {
          bsonType: "string",
          description: "The start timecode of the video range to extract."
        },
          screenshot_path: {
          bsonType: "string",
          description: "The path to the saved screenshot."
        }
      }
    }
  }
})
