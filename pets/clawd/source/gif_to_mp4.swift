import Foundation
import AVFoundation
import ImageIO
import CoreGraphics
import CoreVideo

guard CommandLine.arguments.count == 3 else { fatalError("usage: gif_to_mp4 input.gif output.mp4") }
let sourceURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
try? FileManager.default.removeItem(at: outputURL)
guard let source = CGImageSourceCreateWithURL(sourceURL as CFURL, nil),
      let first = CGImageSourceCreateImageAtIndex(source, 0, nil) else { fatalError("cannot read GIF") }
let width = first.width, height = first.height
let writer = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height
])
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
    kCVPixelBufferWidthKey as String: width,
    kCVPixelBufferHeightKey as String: height,
    kCVPixelBufferCGImageCompatibilityKey as String: true,
    kCVPixelBufferCGBitmapContextCompatibilityKey as String: true
])
writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)
for index in 0..<CGImageSourceGetCount(source) {
    while !input.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.01) }
    guard let frame = CGImageSourceCreateImageAtIndex(source, index, nil) else { fatalError("missing frame") }
    var optionalBuffer: CVPixelBuffer?
    let attributes: [String: Any] = [
        kCVPixelBufferCGImageCompatibilityKey as String: true,
        kCVPixelBufferCGBitmapContextCompatibilityKey as String: true
    ]
    guard CVPixelBufferCreate(nil, width, height, kCVPixelFormatType_32ARGB, attributes as CFDictionary, &optionalBuffer) == kCVReturnSuccess,
          let buffer = optionalBuffer else { fatalError("pixel buffer failed") }
    CVPixelBufferLockBaseAddress(buffer, [])
    guard let context = CGContext(data: CVPixelBufferGetBaseAddress(buffer), width: width, height: height,
                                  bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
                                  space: CGColorSpaceCreateDeviceRGB(),
                                  bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue) else { fatalError("context failed") }
    context.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    context.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.translateBy(x: 0, y: CGFloat(height))
    context.scaleBy(x: 1, y: -1)
    context.draw(frame, in: CGRect(x: 0, y: 0, width: width, height: height))
    CVPixelBufferUnlockBaseAddress(buffer, [])
    let time = CMTime(value: Int64(index), timescale: 6)
    guard adaptor.append(buffer, withPresentationTime: time) else { fatalError("append failed: \(writer.error?.localizedDescription ?? "unknown")") }
}
input.markAsFinished()
let semaphore = DispatchSemaphore(value: 0)
writer.finishWriting { semaphore.signal() }
semaphore.wait()
guard writer.status == .completed else { fatalError(writer.error?.localizedDescription ?? "writer failed") }
print(outputURL.path)
