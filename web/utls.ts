import { Response } from "express"

export function send400(res: Response, data: any) {
  res.status(400).json({ code: 400, data })
}

export function send500(res: Response) {
  res.status(500).json({ code: 500, message: "Internal server error" })
}

export function send200(res: Response, data: any) {
  res.status(200).json({ code: 200, data })
}